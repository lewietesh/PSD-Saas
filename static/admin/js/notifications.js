/**
 * Admin Notification System
 * Polls the API for unreplied messages and displays notifications
 */

(function () {
          'use strict';

          // Configuration
          const CONFIG = {
                    apiUrl: '/api/v1/notifications/admin-summary/',
                    pollInterval: 60000, // 60 seconds
                    maxMessages: 10
          };

          // State
          let notificationData = null;
          let isDropdownOpen = false;
          let pollTimer = null;

          // Initialize when DOM is ready
          document.addEventListener('DOMContentLoaded', function () {
                    initNotifications();
          });

          /**
           * Initialize the notification system
           */
          function initNotifications() {
                    createNotificationBell();
                    fetchNotifications();
                    startPolling();
                    setupClickOutside();
          }

          /**
           * Create the notification bell element in the navbar
           */
          function createNotificationBell() {
                    // Find the navbar - Jazzmin uses AdminLTE structure
                    const navbar = document.querySelector('.main-header .navbar-nav.ml-auto') ||
                              document.querySelector('.main-header .navbar-nav:last-child') ||
                              document.querySelector('.navbar-nav');

                    if (!navbar) {
                              console.warn('Notification: Could not find navbar');
                              return;
                    }

                    // Create notification wrapper
                    const wrapper = document.createElement('li');
                    wrapper.className = 'nav-item notification-wrapper';
                    wrapper.innerHTML = `
            <a class="nav-link notification-bell" href="#" role="button" aria-label="Notifications">
                <i class="fas fa-bell"></i>
                <span class="notification-badge hidden">0</span>
            </a>
            <div class="notification-dropdown">
                <div class="notification-header">
                    <span>Notifications</span>
                    <span class="badge">0 unreplied</span>
                </div>
                <div class="notification-content">
                    <div class="notification-loading">
                        <div class="spinner"></div>
                        <p>Loading...</p>
                    </div>
                </div>
            </div>
        `;

                    // Insert before user menu (usually last item)
                    const userMenu = navbar.querySelector('.nav-item.dropdown') || navbar.lastElementChild;
                    if (userMenu) {
                              navbar.insertBefore(wrapper, userMenu);
                    } else {
                              navbar.appendChild(wrapper);
                    }

                    // Add click handler
                    const bell = wrapper.querySelector('.notification-bell');
                    bell.addEventListener('click', function (e) {
                              e.preventDefault();
                              e.stopPropagation();
                              toggleDropdown();
                    });
          }

          /**
           * Toggle the dropdown visibility
           */
          function toggleDropdown() {
                    const dropdown = document.querySelector('.notification-dropdown');
                    if (!dropdown) return;

                    isDropdownOpen = !isDropdownOpen;
                    dropdown.classList.toggle('show', isDropdownOpen);

                    if (isDropdownOpen) {
                              renderDropdownContent();
                    }
          }

          /**
           * Close dropdown when clicking outside
           */
          function setupClickOutside() {
                    document.addEventListener('click', function (e) {
                              const wrapper = document.querySelector('.notification-wrapper');
                              if (wrapper && !wrapper.contains(e.target) && isDropdownOpen) {
                                        isDropdownOpen = false;
                                        document.querySelector('.notification-dropdown')?.classList.remove('show');
                              }
                    });
          }

          /**
           * Fetch notifications from API
           */
          async function fetchNotifications() {
                    try {
                              const response = await fetch(CONFIG.apiUrl, {
                                        method: 'GET',
                                        headers: {
                                                  'Accept': 'application/json',
                                                  'X-Requested-With': 'XMLHttpRequest'
                                        },
                                        credentials: 'same-origin'
                              });

                              if (!response.ok) {
                                        throw new Error(`HTTP ${response.status}`);
                              }

                              notificationData = await response.json();
                              updateBadge();

                              if (isDropdownOpen) {
                                        renderDropdownContent();
                              }

                    } catch (error) {
                              console.error('Notification fetch error:', error);
                              notificationData = null;
                    }
          }

          /**
           * Start polling for notifications
           */
          function startPolling() {
                    if (pollTimer) {
                              clearInterval(pollTimer);
                    }
                    pollTimer = setInterval(fetchNotifications, CONFIG.pollInterval);
          }

          /**
           * Update the notification badge count
           */
          function updateBadge() {
                    const badge = document.querySelector('.notification-badge');
                    if (!badge) return;

                    const count = notificationData?.summary?.total_unreplied || 0;
                    badge.textContent = count > 99 ? '99+' : count;
                    badge.classList.toggle('hidden', count === 0);

                    // Also update header badge
                    const headerBadge = document.querySelector('.notification-header .badge');
                    if (headerBadge) {
                              headerBadge.textContent = `${count} unreplied`;
                    }
          }

          /**
           * Render dropdown content with notifications
           */
          function renderDropdownContent() {
                    const content = document.querySelector('.notification-content');
                    if (!content || !notificationData) return;

                    const summary = notificationData.summary || {};
                    const messages = notificationData.recent_messages || [];

                    let html = `
            <div class="notification-summary">
                <div class="summary-item">
                    <span class="count">${summary.contact_messages?.unreplied || 0}</span>
                    <span class="label">Contact</span>
                </div>
                <div class="summary-item">
                    <span class="count">${summary.general_messages?.unreplied || 0}</span>
                    <span class="label">General</span>
                </div>
                <div class="summary-item">
                    <span class="count">${summary.user_messages?.unreplied || 0}</span>
                    <span class="label">User</span>
                </div>
            </div>
        `;

                    if (messages.length > 0) {
                              html += '<div class="notification-list">';
                              messages.forEach(msg => {
                                        const url = getMessageUrl(msg);
                                        const typeBadge = getTypeBadge(msg.type);
                                        const timeAgo = formatTimeAgo(msg.created_at);

                                        html += `
                    <a href="${url}" class="notification-item">
                        <div class="sender">
                            ${escapeHtml(msg.sender_name || msg.name || 'Unknown')}
                            <span class="type-badge ${msg.type}">${typeBadge}</span>
                        </div>
                        <div class="subject">${escapeHtml(msg.subject || msg.message?.substring(0, 50) || 'No subject')}</div>
                        <div class="time">${timeAgo}</div>
                    </a>
                `;
                              });
                              html += '</div>';
                    } else {
                              html += `
                <div class="notification-empty">
                    <i class="fas fa-check-circle"></i>
                    <p>No unreplied messages</p>
                </div>
            `;
                    }

                    html += `
            <div class="notification-footer">
                <a href="/admin/notifications/message/">View All Messages</a>
            </div>
        `;

                    content.innerHTML = html;
          }

          /**
           * Get admin URL for a message
           */
          function getMessageUrl(msg) {
                    switch (msg.type) {
                              case 'contact':
                                        return `/admin/notifications/contactmessage/${msg.id}/change/`;
                              case 'general':
                                        return `/admin/notifications/generalmessage/${msg.id}/change/`;
                              case 'user':
                                        return `/admin/notifications/message/${msg.id}/change/`;
                              default:
                                        return `/admin/notifications/message/${msg.id}/change/`;
                    }
          }

          /**
           * Get badge text for message type
           */
          function getTypeBadge(type) {
                    switch (type) {
                              case 'contact': return 'Contact';
                              case 'general': return 'General';
                              case 'user': return 'User';
                              default: return type;
                    }
          }

          /**
           * Format timestamp to relative time
           */
          function formatTimeAgo(dateString) {
                    if (!dateString) return '';

                    const date = new Date(dateString);
                    const now = new Date();
                    const diffMs = now - date;
                    const diffMins = Math.floor(diffMs / 60000);
                    const diffHours = Math.floor(diffMs / 3600000);
                    const diffDays = Math.floor(diffMs / 86400000);

                    if (diffMins < 1) return 'Just now';
                    if (diffMins < 60) return `${diffMins}m ago`;
                    if (diffHours < 24) return `${diffHours}h ago`;
                    if (diffDays < 7) return `${diffDays}d ago`;

                    return date.toLocaleDateString();
          }

          /**
           * Escape HTML to prevent XSS
           */
          function escapeHtml(text) {
                    if (!text) return '';
                    const div = document.createElement('div');
                    div.textContent = text;
                    return div.innerHTML;
          }

})();
