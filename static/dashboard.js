// Advanced Dashboard JavaScript
// Additional interactive features and utilities

class DashboardManager {
    constructor() {
        this.alerts = [];
        this.stats = {
            total: 0,
            active: 0,
            critical: 0,
            resolved: 0
        };
        this.refreshInterval = null;
        this.notifications = [];
        this.init();
    }

    init() {
        this.setupEventListeners();
        this.setupKeyboardShortcuts();
        this.setupNotifications();
        this.startAutoRefresh();
        this.loadInitialData();
    }

    setupEventListeners() {
        // Refresh button
        document.addEventListener('click', (e) => {
            if (e.target.matches('[data-action="refresh"]')) {
                this.refreshAll();
            }
        });

        // Alert filtering
        document.addEventListener('change', (e) => {
            if (e.target.matches('[data-filter]')) {
                this.filterAlerts(e.target.value);
            }
        });

        // Alert details modal
        document.addEventListener('click', (e) => {
            if (e.target.closest('.alert-item')) {
                const alertId = e.target.closest('.alert-item').dataset.alertId;
                this.showAlertDetails(alertId);
            }
        });
    }

    setupKeyboardShortcuts() {
        document.addEventListener('keydown', (e) => {
            // Ctrl/Cmd + R: Refresh
            if ((e.ctrlKey || e.metaKey) && e.key === 'r') {
                e.preventDefault();
                this.refreshAll();
            }
            
            // Ctrl/Cmd + F: Focus search
            if ((e.ctrlKey || e.metaKey) && e.key === 'f') {
                e.preventDefault();
                this.focusSearch();
            }
            
            // Escape: Close modals
            if (e.key === 'Escape') {
                this.closeModals();
            }
        });
    }

    setupNotifications() {
        // Create notification container
        const notificationContainer = document.createElement('div');
        notificationContainer.id = 'notification-container';
        notificationContainer.style.cssText = `
            position: fixed;
            top: 20px;
            right: 20px;
            z-index: 1000;
            display: flex;
            flex-direction: column;
            gap: 10px;
        `;
        document.body.appendChild(notificationContainer);
    }

    showNotification(message, type = 'info', duration = 3000) {
        const notification = document.createElement('div');
        notification.className = `notification ${type}`;
        notification.innerHTML = `
            <div style="display: flex; align-items: center; gap: 10px;">
                <i class="fas fa-${this.getNotificationIcon(type)}"></i>
                <span>${message}</span>
                <button onclick="this.parentElement.parentElement.remove()" style="background: none; border: none; color: #666; cursor: pointer;">
                    <i class="fas fa-times"></i>
                </button>
            </div>
        `;
        
        document.getElementById('notification-container').appendChild(notification);
        
        // Auto remove
        setTimeout(() => {
            if (notification.parentElement) {
                notification.remove();
            }
        }, duration);
    }

    getNotificationIcon(type) {
        const icons = {
            success: 'check-circle',
            error: 'exclamation-circle',
            warning: 'exclamation-triangle',
            info: 'info-circle'
        };
        return icons[type] || 'info-circle';
    }

    async loadInitialData() {
        try {
            await Promise.all([
                this.checkHealth(),
                this.loadAlerts()
            ]);
            this.showNotification('Dashboard loaded successfully', 'success');
        } catch (error) {
            this.showNotification('Failed to load dashboard data', 'error');
        }
    }

    async checkHealth() {
        try {
            const response = await fetch('/health');
            const data = await response.json();
            
            this.updateStatusIndicator(response.ok, data);
            return response.ok;
        } catch (error) {
            this.updateStatusIndicator(false, null);
            return false;
        }
    }

    updateStatusIndicator(isOnline, data) {
        const statusDot = document.getElementById('status-dot');
        const statusText = document.getElementById('status-text');
        const statusTime = document.getElementById('status-time');
        
        if (isOnline) {
            statusDot.className = 'status-dot online';
            statusText.textContent = 'Online';
            statusTime.textContent = `Last checked: ${new Date(data.time).toLocaleString()}`;
        } else {
            statusDot.className = 'status-dot offline';
            statusText.textContent = 'Offline';
            statusTime.textContent = 'Connection failed';
        }
    }

    async loadAlerts() {
        try {
            const response = await fetch('/alerts?limit=20');
            const alerts = await response.json();
            
            this.alerts = alerts;
            this.updateStats();
            this.renderAlerts();
            
            return alerts;
        } catch (error) {
            this.renderError('Failed to load alerts');
            throw error;
        }
    }

    updateStats() {
        this.stats.total = this.alerts.length;
        this.stats.active = this.alerts.filter(a => 
            a.alert_level === 'CRITICAL' || a.alert_level === 'WARNING'
        ).length;
        this.stats.critical = this.alerts.filter(a => 
            a.alert_level === 'CRITICAL'
        ).length;
        this.stats.resolved = this.alerts.filter(a => 
            a.alert_level === 'INFO'
        ).length;

        // Update UI
        document.getElementById('total-alerts').textContent = this.stats.total;
        document.getElementById('active-alerts').textContent = this.stats.active;
        document.getElementById('critical-alerts').textContent = this.stats.critical;

        // Animate stats
        this.animateStats();
    }

    animateStats() {
        const statNumbers = document.querySelectorAll('.stat-number');
        statNumbers.forEach(stat => {
            stat.style.transform = 'scale(1.1)';
            setTimeout(() => {
                stat.style.transform = 'scale(1)';
            }, 200);
        });
    }

    renderAlerts() {
        const container = document.getElementById('alerts-container');
        container.innerHTML = '';

        if (this.alerts.length === 0) {
            this.renderNoAlerts();
            return;
        }

        this.alerts.forEach((alert, index) => {
            const alertElement = this.createAlertElement(alert, index);
            container.appendChild(alertElement);
        });
    }

    createAlertElement(alert, index) {
        const alertDiv = document.createElement('div');
        alertDiv.className = `alert-item ${alert.alert_level.toLowerCase()}`;
        alertDiv.dataset.alertId = alert.alert_id;
        alertDiv.style.animationDelay = `${index * 0.1}s`;

        const timeAgo = this.getTimeAgo(new Date(alert.timestamp));
        const confidence = (alert.confidence_score * 100).toFixed(1);

        alertDiv.innerHTML = `
            <div class="alert-header">
                <div>
                    <strong>${alert.anomaly_type}</strong>
                    <span class="alert-level ${alert.alert_level.toLowerCase()}">${alert.alert_level}</span>
                </div>
                <div style="font-size: 0.8rem; color: #666;">
                    ${timeAgo}
                </div>
            </div>
            <div class="alert-details">
                <div class="alert-detail">
                    <div class="alert-detail-label">Tourist ID</div>
                    <div class="alert-detail-value">${alert.tourist_id}</div>
                </div>
                <div class="alert-detail">
                    <div class="alert-detail-label">Confidence</div>
                    <div class="alert-detail-value">${confidence}%</div>
                </div>
                <div class="alert-detail">
                    <div class="alert-detail-label">Location</div>
                    <div class="alert-detail-value">${alert.latitude.toFixed(4)}, ${alert.longitude.toFixed(4)}</div>
                </div>
                <div class="alert-detail">
                    <div class="alert-detail-label">Time</div>
                    <div class="alert-detail-value">${new Date(alert.timestamp).toLocaleString()}</div>
                </div>
            </div>
        `;

        return alertDiv;
    }

    renderNoAlerts() {
        const container = document.getElementById('alerts-container');
        container.innerHTML = `
            <div class="no-alerts">
                <i class="fas fa-check-circle"></i>
                <h3>No alerts found</h3>
                <p>System is running smoothly</p>
            </div>
        `;
    }

    renderError(message) {
        const container = document.getElementById('alerts-container');
        container.innerHTML = `
            <div class="no-alerts">
                <i class="fas fa-exclamation-triangle"></i>
                <h3>Error</h3>
                <p>${message}</p>
            </div>
        `;
    }

    getTimeAgo(date) {
        const now = new Date();
        const diff = now - date;
        const minutes = Math.floor(diff / 60000);
        const hours = Math.floor(diff / 3600000);
        const days = Math.floor(diff / 86400000);

        if (minutes < 1) return 'Just now';
        if (minutes < 60) return `${minutes}m ago`;
        if (hours < 24) return `${hours}h ago`;
        return `${days}d ago`;
    }

    filterAlerts(filter) {
        const alerts = document.querySelectorAll('.alert-item');
        
        alerts.forEach(alert => {
            const level = alert.classList.contains('critical') ? 'critical' :
                         alert.classList.contains('warning') ? 'warning' : 'info';
            
            if (filter === 'all' || level === filter) {
                alert.style.display = 'block';
            } else {
                alert.style.display = 'none';
            }
        });
    }

    showAlertDetails(alertId) {
        const alert = this.alerts.find(a => a.alert_id === alertId);
        if (!alert) return;

        // Create modal
        const modal = document.createElement('div');
        modal.className = 'modal';
        modal.innerHTML = `
            <div class="modal-content">
                <div class="modal-header">
                    <h3>Alert Details</h3>
                    <button class="modal-close">&times;</button>
                </div>
                <div class="modal-body">
                    <pre>${JSON.stringify(alert, null, 2)}</pre>
                </div>
            </div>
        `;

        // Add modal styles
        modal.style.cssText = `
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: rgba(0, 0, 0, 0.5);
            display: flex;
            justify-content: center;
            align-items: center;
            z-index: 1000;
        `;

        document.body.appendChild(modal);

        // Close modal handlers
        modal.querySelector('.modal-close').onclick = () => modal.remove();
        modal.onclick = (e) => {
            if (e.target === modal) modal.remove();
        };
    }

    refreshAll() {
        const refreshBtn = document.querySelector('button[onclick="refreshAll()"]');
        if (refreshBtn) {
            const originalText = refreshBtn.innerHTML;
            refreshBtn.innerHTML = '<i class="fas fa-sync-alt fa-spin"></i> Refreshing...';
            refreshBtn.disabled = true;

            Promise.all([this.checkHealth(), this.loadAlerts()])
                .then(() => {
                    this.showNotification('Data refreshed successfully', 'success');
                })
                .catch(() => {
                    this.showNotification('Failed to refresh data', 'error');
                })
                .finally(() => {
                    setTimeout(() => {
                        refreshBtn.innerHTML = originalText;
                        refreshBtn.disabled = false;
                    }, 1000);
                });
        }
    }

    startAutoRefresh() {
        this.refreshInterval = setInterval(() => {
            this.checkHealth();
            this.loadAlerts();
        }, 30000);
    }

    stopAutoRefresh() {
        if (this.refreshInterval) {
            clearInterval(this.refreshInterval);
            this.refreshInterval = null;
        }
    }

    closeModals() {
        const modals = document.querySelectorAll('.modal');
        modals.forEach(modal => modal.remove());
    }

    focusSearch() {
        const searchInput = document.querySelector('[data-search]');
        if (searchInput) {
            searchInput.focus();
        }
    }
}

// Initialize dashboard when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    window.dashboard = new DashboardManager();
});

// Export for global access
window.DashboardManager = DashboardManager;
