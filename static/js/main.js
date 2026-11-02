// AgriSure Main Client & Real-time Integration
document.addEventListener("DOMContentLoaded", function () {
    initLiveNotifications();
    initPriceCalculators();
});

// Real-Time Notification Handler with WebSocket & Fallback
function initLiveNotifications() {
    const badge = document.getElementById("notif-badge");
    const dropdownList = document.getElementById("notif-dropdown-items");

    // Check if WebSocket is supported
    const protocol = window.location.protocol === "https:" ? "wss://" : "ws://";
    const wsUrl = protocol + window.location.host + "/ws/notifications/";

    let socket = null;
    try {
        socket = new WebSocket(wsUrl);

        socket.onmessage = function (event) {
            const data = JSON.parse(event.data);
            if (data.type === "notification") {
                showToastNotification(data.title, data.message, data.link_url);
                updateUnreadCount(1);
            }
        };

        socket.onerror = function () {
            // If websocket encounters error, fallback to polling
            startNotificationPolling();
        };
    } catch (e) {
        startNotificationPolling();
    }

    // Polling fallback every 10 seconds
    function startNotificationPolling() {
        setInterval(function () {
            fetch("/notifications/api/unread/")
                .then(res => res.json())
                .then(data => {
                    if (badge) {
                        if (data.unread_count > 0) {
                            badge.textContent = data.unread_count;
                            badge.classList.remove("d-none");
                        } else {
                            badge.classList.add("d-none");
                        }
                    }
                })
                .catch(() => {});
        }, 10000);
    }
}

function updateUnreadCount(increment) {
    const badge = document.getElementById("notif-badge");
    if (badge) {
        let current = parseInt(badge.textContent) || 0;
        let updated = current + increment;
        badge.textContent = updated;
        badge.classList.remove("d-none");
    }
}

function showToastNotification(title, message, link) {
    const container = document.getElementById("toast-container");
    if (!container) return;

    const toastEl = document.createElement("div");
    toastEl.className = "toast align-items-center text-bg-success border-0 show shadow-lg mb-2";
    toastEl.setAttribute("role", "alert");
    toastEl.innerHTML = `
        <div class="d-flex">
            <div class="toast-body">
                <strong><i class="bi bi-bell-fill me-1"></i> ${title}</strong>
                <div class="small mt-1">${message}</div>
                ${link ? `<a href="${link}" class="btn btn-sm btn-light text-success fw-bold mt-2 py-0">View Details</a>` : ''}
            </div>
            <button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast"></button>
        </div>
    `;
    container.appendChild(toastEl);

    setTimeout(() => {
        toastEl.remove();
    }, 8000);
}

// Live Commercial Terms Dynamic Calculator
function initPriceCalculators() {
    const qtyInput = document.getElementById("id_quantity_kg") || document.getElementById("id_total_quantity_kg");
    const priceInput = document.getElementById("id_proposed_price_per_kg") || document.getElementById("id_expected_price_per_kg");
    const totalDisplay = document.getElementById("calc-total-display");

    if (qtyInput && priceInput && totalDisplay) {
        function calculate() {
            const q = parseFloat(qtyInput.value) || 0;
            const p = parseFloat(priceInput.value) || 0;
            const total = q * p;
            totalDisplay.textContent = "₹ " + total.toLocaleString("en-IN", { minimumFractionDigits: 2, maximumFractionDigits: 2 });
        }
        qtyInput.addEventListener("input", calculate);
        priceInput.addEventListener("input", calculate);
        calculate();
    }
}
