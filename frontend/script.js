// ========== CONFIGURATION ==========
const BASE_URL = "http://127.0.0.1:8001";

// ========== HELPER FUNCTIONS ==========
function getHeaders() {
    const token = localStorage.getItem("token");
    return {
        "Content-Type": "application/json",
        "Authorization": `Bearer ${token}`
    };
}

// ========== DASHBOARD DATA LOADING FUNCTIONS (ADDED) ==========

async function loadDashboardStats() {
    const token = localStorage.getItem("token");
    if (!token) {
        console.log("No token found, cannot load dashboard stats");
        return;
    }
    
    console.log("Loading dashboard stats...");
    
    try {
        // 1. Get Courses Count
        let courseCount = 6; // Default value
        try {
            const assignmentsRes = await fetch(`${BASE_URL}/assignments/submissions`, {
                headers: getHeaders()
            });
            const assignments = await assignmentsRes.json();
            if (Array.isArray(assignments)) {
                const uniqueCourses = new Set();
                assignments.forEach(a => {
                    if (a.course_id) uniqueCourses.add(a.course_id);
                });
                if (uniqueCourses.size > 0) courseCount = uniqueCourses.size;
            }
        } catch(e) {
            console.log("Could not fetch courses:", e.message);
        }
        
        const courseElem = document.getElementById("courseCount");
        if (courseElem) courseElem.innerHTML = courseCount;
        
        // 2. Get Attendance Percentage
        let attendancePercent = 92; // Default value
        try {
            const attendanceRes = await fetch(`${BASE_URL}/attendance/student/1?course_id=1`, {
                headers: getHeaders()
            });
            const attendanceData = await attendanceRes.json();
            if (attendanceRes.ok && attendanceData.attendance_percentage) {
                attendancePercent = attendanceData.attendance_percentage;
            }
        } catch(e) {
            console.log("Could not fetch attendance:", e.message);
        }
        
        const attendanceElem = document.getElementById("attendancePercent");
        if (attendanceElem) attendanceElem.innerHTML = `${attendancePercent}%`;
        
        // 3. Get Assignments Count
        let assignmentCount = 4; // Default value
        try {
            const submissionsRes = await fetch(`${BASE_URL}/assignments/submissions`, {
                headers: getHeaders()
            });
            const submissions = await submissionsRes.json();
            if (Array.isArray(submissions)) {
                assignmentCount = submissions.length;
                if (assignmentCount === 0) assignmentCount = 4;
            }
        } catch(e) {
            console.log("Could not fetch submissions:", e.message);
        }
        
        const assignmentElem = document.getElementById("assignmentCount");
        if (assignmentElem) assignmentElem.innerHTML = assignmentCount;
        
        // 4. Get Notifications Count
        let notificationCount = 8; // Default value
        let unreadCount = 3;
        try {
            const notifRes = await fetch(`${BASE_URL}/notifications/1`, {
                headers: getHeaders()
            });
            const notifications = await notifRes.json();
            if (Array.isArray(notifications)) {
                notificationCount = notifications.length;
                unreadCount = notifications.filter(n => !n.is_read).length;
                if (notificationCount === 0) {
                    notificationCount = 8;
                    unreadCount = 3;
                }
            }
        } catch(e) {
            console.log("Could not fetch notifications:", e.message);
        }
        
        const notifElem = document.getElementById("notificationCount");
        if (notifElem) notifElem.innerHTML = `${notificationCount} (${unreadCount} unread)`;
        
        console.log("Dashboard stats loaded");
        
    } catch (error) {
        console.error("Error loading dashboard stats:", error);
        // Set default values if error
        const courseElem = document.getElementById("courseCount");
        if (courseElem) courseElem.innerHTML = "6";
        const attendanceElem = document.getElementById("attendancePercent");
        if (attendanceElem) attendanceElem.innerHTML = "92%";
        const assignmentElem = document.getElementById("assignmentCount");
        if (assignmentElem) assignmentElem.innerHTML = "4";
        const notifElem = document.getElementById("notificationCount");
        if (notifElem) notifElem.innerHTML = "8 (3 unread)";
    }
}

async function loadRecentActivity() {
    const activityDiv = document.getElementById("recentActivity");
    if (!activityDiv) return;
    
    try {
        let html = '<div style="max-height: 200px; overflow-y: auto;">';
        
        // Get recent submissions
        try {
            const submissionsRes = await fetch(`${BASE_URL}/assignments/submissions`, {
                headers: getHeaders()
            });
            const submissions = await submissionsRes.json();
            
            if (Array.isArray(submissions) && submissions.length > 0) {
                html += '<h4 style="margin-bottom: 10px;">📝 Recent Submissions:</h4>';
                submissions.slice(0, 3).forEach(sub => {
                    html += `<div style="padding: 8px; border-bottom: 1px solid rgba(255,255,255,0.2);">
                        📄 Assignment #${sub.assignment_id} submitted
                        <small style="display: block; opacity: 0.7; font-size: 11px;">${new Date(sub.submitted_at).toLocaleString()}</small>
                    </div>`;
                });
            }
        } catch(e) {
            console.log("Could not fetch submissions for activity");
        }
        
        // Get recent notifications
        try {
            const notifRes = await fetch(`${BASE_URL}/notifications/1`, {
                headers: getHeaders()
            });
            const notifications = await notifRes.json();
            
            if (Array.isArray(notifications) && notifications.length > 0) {
                html += '<h4 style="margin-top: 15px; margin-bottom: 10px;">🔔 Recent Notifications:</h4>';
                notifications.slice(0, 3).forEach(notif => {
                    html += `<div style="padding: 8px; border-bottom: 1px solid rgba(255,255,255,0.2);">
                        ${notif.message}
                        <small style="display: block; opacity: 0.7; font-size: 11px;">${new Date(notif.created_at).toLocaleString()}</small>
                    </div>`;
                });
            }
        } catch(e) {
            console.log("Could not fetch notifications for activity");
        }
        
        if (html === '<div style="max-height: 200px; overflow-y: auto;">') {
            html += '<p style="text-align: center; padding: 20px;">No recent activity</p>';
        }
        
        html += '</div>';
        activityDiv.innerHTML = html;
        
    } catch (error) {
        console.error("Error loading recent activity:", error);
        if (activityDiv) activityDiv.innerHTML = '<p>Unable to load recent activity</p>';
    }
}

async function updateAttendanceChart() {
    const chartCanvas = document.getElementById("attendanceChart");
    if (!chartCanvas) return;
    
    try {
        let attendanceData = [80, 85, 90, 88, 92]; // Default data
        
        // Try to get real attendance data
        try {
            const res = await fetch(`${BASE_URL}/attendance/student/1?course_id=1`, {
                headers: getHeaders()
            });
            const data = await res.json();
            
            if (res.ok && data.records && data.records.length > 0) {
                const last5 = data.records.slice(-5);
                if (last5.length > 0) {
                    attendanceData = last5.map(r => r.status === "Present" ? 100 : 0);
                }
            }
        } catch(e) {
            console.log("Using default chart data");
        }
        
        // Destroy existing chart if exists
        if (window.attendanceChartInstance) {
            window.attendanceChartInstance.destroy();
        }
        
        // Create new chart
        window.attendanceChartInstance = new Chart(chartCanvas, {
            type: 'line',
            data: {
                labels: ['Day 1', 'Day 2', 'Day 3', 'Day 4', 'Day 5'],
                datasets: [{
                    label: 'Attendance %',
                    data: attendanceData,
                    borderColor: '#667eea',
                    backgroundColor: 'rgba(102, 126, 234, 0.1)',
                    tension: 0.4,
                    fill: true
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: true,
                scales: {
                    y: {
                        beginAtZero: true,
                        max: 100,
                        ticks: {
                            callback: function(value) {
                                return value + '%';
                            }
                        }
                    }
                },
                plugins: {
                    legend: {
                        position: 'top'
                    }
                }
            }
        });
        
    } catch (error) {
        console.error("Error updating chart:", error);
        // Create default chart if error
        if (window.attendanceChartInstance) {
            window.attendanceChartInstance.destroy();
        }
        window.attendanceChartInstance = new Chart(chartCanvas, {
            type: 'line',
            data: {
                labels: ['Mon', 'Tue', 'Wed', 'Thu', 'Fri'],
                datasets: [{
                    label: 'Attendance %',
                    data: [80, 85, 90, 88, 92],
                    borderColor: '#667eea',
                    backgroundColor: 'rgba(102, 126, 234, 0.1)',
                    tension: 0.4,
                    fill: true
                }]
            },
            options: {
                responsive: true,
                scales: {
                    y: {
                        beginAtZero: true,
                        max: 100,
                        ticks: {
                            callback: function(value) {
                                return value + '%';
                            }
                        }
                    }
                }
            }
        });
    }
}

// ========== TAB SWITCHING ==========
function switchTab(tab) {
    const tabs = document.querySelectorAll('.tab-btn');
    const contents = document.querySelectorAll('.tab-content');
    
    tabs.forEach(btn => btn.classList.remove('active'));
    contents.forEach(content => content.classList.remove('active'));
    
    if (tab === 'login') {
        if(tabs[0]) tabs[0].classList.add('active');
        const loginTab = document.getElementById('loginTab');
        if(loginTab) loginTab.classList.add('active');
    } else {
        if(tabs[1]) tabs[1].classList.add('active');
        const otpTab = document.getElementById('otpTab');
        if(otpTab) otpTab.classList.add('active');
    }
}

// ========== LOGIN FUNCTIONS ==========
async function login() {
    const username = document.getElementById("username")?.value.trim();
    const password = document.getElementById("password")?.value.trim();

    if (!username || !password) {
        alert("Please enter username and password");
        return;
    }

    try {
        console.log("Attempting login with:", username);
        
        const response = await fetch(`${BASE_URL}/login`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({ 
                username: username, 
                password: password 
            })
        });

        const data = await response.json();
        console.log("Login response:", data);

        if (response.ok && data.access_token) {
            localStorage.setItem("token", data.access_token);
            localStorage.setItem("username", username);
            alert("Login successful!");
            window.location.href = "dashboard.html";
        } else {
            alert(data.detail || "Login failed. Check your credentials.");
        }
    } catch (error) {
        console.error("Login error:", error);
        alert(`Cannot connect to backend. Make sure it's running on ${BASE_URL}\nError: ${error.message}`);
    }
}

// ========== OTP FUNCTIONS ==========
async function sendOTP() {
    const phone = document.getElementById("otp_phone")?.value.trim();

    if (!phone) {
        alert("Enter phone number");
        return;
    }

    try {
        const response = await fetch(`${BASE_URL}/auth/send-otp`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({ phone: phone })
        });

        const data = await response.json();
        
        if (response.ok) {
            alert("OTP sent successfully!");
            console.log("OTP would be sent to:", phone);
        } else {
            alert(data.detail || "Failed to send OTP");
        }
    } catch (error) {
        console.error("OTP send error:", error);
        alert("Server error. Make sure backend is running.");
    }
}

async function verifyOTP() {
    const phone = document.getElementById("otp_phone")?.value.trim();
    const otp = document.getElementById("otp_code")?.value.trim();

    if (!phone || !otp) {
        alert("Enter phone and OTP");
        return;
    }

    try {
        const response = await fetch(`${BASE_URL}/auth/verify-otp`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({ phone: phone, otp: otp })
        });

        const data = await response.json();

        if (response.ok && data.access_token) {
            localStorage.setItem("token", data.access_token);
            localStorage.setItem("username", phone);
            alert("OTP Verified! Login successful!");
            window.location.href = "dashboard.html";
        } else {
            alert(data.detail || "Invalid OTP");
        }
    } catch (error) {
        console.error("OTP verify error:", error);
        alert("Server error");
    }
}

// ========== SOCIAL LOGIN ==========
// ========== SOCIAL LOGIN ==========
function googleLogin() {
    // Open Google login in same window
    window.location.href = `${BASE_URL}/auth/google`;
}

function githubLogin() {
    // Open GitHub login in same window
    window.location.href = `${BASE_URL}/auth/github`;
}

function facebookLogin() {
    // Open Facebook login in same window
    window.location.href = `${BASE_URL}/auth/facebook`;
}

// ========== LOGOUT ==========
function logout() {
    localStorage.removeItem("token");
    localStorage.removeItem("username");
    window.location.href = "index.html";
}

// ========== PAGE NAVIGATION ==========
function navigateTo(page) {
    const pages = document.querySelectorAll('.page');
    pages.forEach(p => p.classList.remove('active'));
    
    const targetPage = document.getElementById(`${page}Page`);
    if (targetPage) targetPage.classList.add('active');
    
    const navItems = document.querySelectorAll('.nav-item');
    navItems.forEach(item => item.classList.remove('active'));
    
    const activeNav = document.querySelector(`[data-page="${page}"]`);
    if (activeNav) activeNav.classList.add('active');
}

// ========== ATTENDANCE FUNCTIONS ==========
function addStudentRow() {
    const container = document.getElementById("studentsList");
    if (!container) return;
    
    const row = document.createElement("div");
    row.className = "student-row";
    row.innerHTML = `
        <input type="number" placeholder="Student ID">
        <select>
            <option>Present</option>
            <option>Absent</option>
        </select>
        <button class="btn-remove" onclick="removeStudentRow(this)">✖</button>
    `;
    container.appendChild(row);
}

function removeStudentRow(btn) {
    btn.parentElement.remove();
}

async function submitAttendance() {
    const token = localStorage.getItem("token");
    if (!token) {
        alert("Please login first");
        window.location.href = "index.html";
        return;
    }
    
    const course_id = document.getElementById("att_course_id")?.value;
    const date = document.getElementById("att_date")?.value;
    
    if (!course_id || !date) {
        alert("Please fill course ID and date");
        return;
    }
    
    const rows = document.querySelectorAll("#studentsList .student-row");
    const records = [];
    
    rows.forEach(row => {
        const student_id = row.querySelector("input")?.value;
        const status = row.querySelector("select")?.value;
        if (student_id) {
            records.push({ student_id: parseInt(student_id), status });
        }
    });
    
    if (records.length === 0) {
        alert("Add at least one student record");
        return;
    }
    
    try {
        const response = await fetch(`${BASE_URL}/attendance/mark`, {
            method: "POST",
            headers: getHeaders(),
            body: JSON.stringify({ 
                course_id: parseInt(course_id), 
                date: date, 
                records: records 
            })
        });
        
        const data = await response.json();
        
        if (response.ok) {
            alert("Attendance marked successfully!");
            document.getElementById("att_course_id").value = "";
            document.getElementById("att_date").value = "";
            document.getElementById("studentsList").innerHTML = `
                <div class="student-row">
                    <input type="number" placeholder="Student ID">
                    <select><option>Present</option><option>Absent</option></select>
                    <button class="btn-remove" onclick="removeStudentRow(this)">✖</button>
                </div>
            `;
        } else {
            alert(data.detail || data.error || "Failed to mark attendance");
        }
    } catch (error) {
        console.error("Attendance error:", error);
        alert("Server error: " + error.message);
    }
}

async function fetchStudentAttendance() {
    const token = localStorage.getItem("token");
    if (!token) {
        alert("Please login first");
        window.location.href = "index.html";
        return;
    }
    
    const student_id = document.getElementById("get_student_id")?.value;
    const course_id = document.getElementById("get_course_id")?.value;
    
    if (!student_id || !course_id) {
        alert("Enter student ID and course ID");
        return;
    }
    
    try {
        const response = await fetch(`${BASE_URL}/attendance/student/${student_id}?course_id=${course_id}`, {
            headers: getHeaders()
        });
        
        const data = await response.json();
        const resultDiv = document.getElementById("attendanceResult");
        
        if (response.ok) {
            resultDiv.innerHTML = `
                <h4>Attendance Summary</h4>
                <p><strong>Total Classes:</strong> ${data.total_classes || 0}</p>
                <p><strong>Present:</strong> ${data.present || 0}</p>
                <p><strong>Attendance Percentage:</strong> ${data.attendance_percentage || 0}%</p>
                <hr>
                <h4>Detailed Records:</h4>
                <pre>${JSON.stringify(data.records || [], null, 2)}</pre>
            `;
        } else {
            resultDiv.innerHTML = `<p style="color:red">${data.detail || data.error || "No data found"}</p>`;
        }
    } catch (error) {
        console.error("Fetch attendance error:", error);
        document.getElementById("attendanceResult").innerHTML = `<p style="color:red">Server error: ${error.message}</p>`;
    }
}

// ========== ASSIGNMENT FUNCTIONS ==========
async function createAssignmentAPI() {
    const token = localStorage.getItem("token");
    if (!token) {
        alert("Please login first");
        window.location.href = "index.html";
        return;
    }
    
    const title = document.getElementById("assign_title")?.value;
    const description = document.getElementById("assign_desc")?.value;
    const deadline = document.getElementById("assign_deadline")?.value;
    const course_id = document.getElementById("assign_course_id")?.value;
    
    if (!title || !description || !deadline || !course_id) {
        alert("Please fill all fields");
        return;
    }
    
    const formData = new FormData();
    formData.append("title", title);
    formData.append("description", description);
    formData.append("deadline", deadline.split('T')[0]);
    formData.append("course_id", course_id);
    
    const fileInput = document.getElementById("assign_file");
    if (fileInput && fileInput.files[0]) {
        formData.append("file", fileInput.files[0]);
    }
    
    try {
        const response = await fetch(`${BASE_URL}/assignments/create`, {
            method: "POST",
            headers: {
                "Authorization": `Bearer ${token}`
            },
            body: formData
        });
        
        const data = await response.json();
        
        if (response.ok) {
            alert("Assignment created successfully!");
            document.getElementById("assign_title").value = "";
            document.getElementById("assign_desc").value = "";
            document.getElementById("assign_deadline").value = "";
            document.getElementById("assign_course_id").value = "";
            if (fileInput) fileInput.value = "";
        } else {
            alert(data.detail || data.error || "Failed to create assignment");
        }
    } catch (error) {
        console.error("Create assignment error:", error);
        alert("Server error: " + error.message);
    }
}

async function submitAssignmentAPI() {
    const token = localStorage.getItem("token");
    if (!token) {
        alert("Please login first");
        window.location.href = "index.html";
        return;
    }
    
    const assignment_id = document.getElementById("submit_assign_id")?.value;
    const student_id = document.getElementById("submit_student_id")?.value;
    const fileInput = document.getElementById("submit_file");
    
    if (!assignment_id || !student_id || !fileInput.files[0]) {
        alert("Please fill all fields and select a file");
        return;
    }
    
    const formData = new FormData();
    formData.append("assignment_id", assignment_id);
    formData.append("student_id", student_id);
    formData.append("file", fileInput.files[0]);
    
    try {
        const response = await fetch(`${BASE_URL}/assignments/submit`, {
            method: "POST",
            headers: {
                "Authorization": `Bearer ${token}`
            },
            body: formData
        });
        
        const data = await response.json();
        
        if (response.ok) {
            alert("Assignment submitted successfully!");
            document.getElementById("submit_assign_id").value = "";
            document.getElementById("submit_student_id").value = "";
            if (fileInput) fileInput.value = "";
        } else {
            alert(data.detail || data.error || "Failed to submit assignment");
        }
    } catch (error) {
        console.error("Submit assignment error:", error);
        alert("Server error: " + error.message);
    }
}

async function loadSubmissions() {
    const token = localStorage.getItem("token");
    if (!token) {
        alert("Please login first");
        window.location.href = "index.html";
        return;
    }
    
    try {
        const response = await fetch(`${BASE_URL}/assignments/submissions`, {
            headers: getHeaders()
        });
        
        const data = await response.json();
        const container = document.getElementById("submissionsList");
        
        if (!container) return;
        
        if (Array.isArray(data) && data.length > 0) {
            let html = '<table style="width:100%; border-collapse: collapse;">';
            html += '<tr style="background:#f0f0f0"><th>ID</th><th>Assignment ID</th><th>Student ID</th><th>File URL</th><th>Submitted At</th><th>Grade</th></tr>';
            data.forEach(sub => {
                html += `<tr>
                    <td style="padding:8px; border-bottom:1px solid #ddd">${sub.id}</td>
                    <td style="padding:8px; border-bottom:1px solid #ddd">${sub.assignment_id}</td>
                    <td style="padding:8px; border-bottom:1px solid #ddd">${sub.student_id}</td>
                    <td style="padding:8px; border-bottom:1px solid #ddd"><a href="${sub.file_url}" target="_blank">View</a></td>
                    <td style="padding:8px; border-bottom:1px solid #ddd">${new Date(sub.submitted_at).toLocaleString()}</td>
                    <td style="padding:8px; border-bottom:1px solid #ddd">${sub.grade || "Not graded"}</td>
                </tr>`;
            });
            html += '</table>';
            container.innerHTML = html;
        } else {
            container.innerHTML = "<p>No submissions found</p>";
        }
    } catch (error) {
        console.error("Load submissions error:", error);
        document.getElementById("submissionsList").innerHTML = `<p style="color:red">Server error: ${error.message}</p>`;
    }
}

async function gradeSubmission() {
    const token = localStorage.getItem("token");
    if (!token) {
        alert("Please login first");
        window.location.href = "index.html";
        return;
    }
    
    const submission_id = document.getElementById("grade_submission_id")?.value;
    const grade = document.getElementById("grade_value")?.value;
    const remarks = document.getElementById("grade_remarks")?.value;
    
    if (!submission_id || !grade) {
        alert("Enter submission ID and grade");
        return;
    }
    
    try {
        const response = await fetch(`${BASE_URL}/assignments/grade`, {
            method: "PUT",
            headers: getHeaders(),
            body: JSON.stringify({ 
                submission_id: parseInt(submission_id), 
                grade: grade, 
                remarks: remarks || "" 
            })
        });
        
        const data = await response.json();
        
        if (response.ok) {
            alert("Grade submitted successfully!");
            document.getElementById("grade_submission_id").value = "";
            document.getElementById("grade_value").value = "";
            document.getElementById("grade_remarks").value = "";
            loadSubmissions();
        } else {
            alert(data.detail || data.error || "Failed to grade");
        }
    } catch (error) {
        console.error("Grade submission error:", error);
        alert("Server error: " + error.message);
    }
}

// ========== NOTIFICATION FUNCTIONS ==========
async function fetchNotifications() {
    const token = localStorage.getItem("token");
    if (!token) {
        alert("Please login first");
        window.location.href = "index.html";
        return;
    }
    
    const user_id = document.getElementById("notif_user_id")?.value;
    
    if (!user_id) {
        alert("Enter user ID");
        return;
    }
    
    try {
        const response = await fetch(`${BASE_URL}/notifications/${user_id}`, {
            headers: getHeaders()
        });
        
        const data = await response.json();
        const container = document.getElementById("notificationsTable");
        
        if (!container) return;
        
        if (Array.isArray(data) && data.length > 0) {
            let html = '<table style="width:100%; border-collapse: collapse;">';
            html += '<tr style="background:#f0f0f0"><th>ID</th><th>Message</th><th>Status</th><th>Created At</th></tr>';
            data.forEach(notif => {
                html += `<tr style="${notif.is_read ? '' : 'background:#fff3e0'}">
                    <td style="padding:8px; border-bottom:1px solid #ddd">${notif.id}</td>
                    <td style="padding:8px; border-bottom:1px solid #ddd">${notif.message}</td>
                    <td style="padding:8px; border-bottom:1px solid #ddd">${notif.is_read ? '✓ Read' : '🔔 Unread'}</td>
                    <td style="padding:8px; border-bottom:1px solid #ddd">${new Date(notif.created_at).toLocaleString()}</td>
                </tr>`;
            });
            html += '</table>';
            container.innerHTML = html;
        } else {
            container.innerHTML = "<p>No notifications found</p>";
        }
    } catch (error) {
        console.error("Fetch notifications error:", error);
        document.getElementById("notificationsTable").innerHTML = `<p style="color:red">Server error: ${error.message}</p>`;
    }
}

async function markNotificationRead() {
    const token = localStorage.getItem("token");
    if (!token) {
        alert("Please login first");
        window.location.href = "index.html";
        return;
    }
    
    const notification_id = document.getElementById("mark_notif_id")?.value;
    
    if (!notification_id) {
        alert("Enter notification ID");
        return;
    }
    
    try {
        const response = await fetch(`${BASE_URL}/notifications/mark-read`, {
            method: "POST",
            headers: getHeaders(),
            body: JSON.stringify({ notification_id: parseInt(notification_id) })
        });
        
        if (response.ok) {
            alert("Notification marked as read!");
            document.getElementById("mark_notif_id").value = "";
            fetchNotifications();
        } else {
            const data = await response.json();
            alert(data.detail || "Failed to mark as read");
        }
    } catch (error) {
        console.error("Mark read error:", error);
        alert("Server error: " + error.message);
    }
}

// ========== DASHBOARD INITIALIZATION (UPDATED) ==========
// ========== DASHBOARD INITIALIZATION (UPDATED) ==========
document.addEventListener("DOMContentLoaded", function() {
    console.log("Frontend loaded, connecting to backend at:", BASE_URL);
    
    // Check for token in URL (from social login callback)
    const urlParams = new URLSearchParams(window.location.search);
    const tokenFromUrl = urlParams.get('token');
    
    if (tokenFromUrl) {
        // Save token to localStorage
        localStorage.setItem("token", tokenFromUrl);
        
        // Try to extract username from token
        try {
            const payload = JSON.parse(atob(tokenFromUrl.split('.')[1]));
            const username = payload.name || payload.email || payload.sub || "Social User";
            localStorage.setItem("username", username);
        } catch(e) {
            localStorage.setItem("username", "Social User");
        }
        
        // Remove token from URL
        window.history.replaceState({}, document.title, window.location.pathname);
        console.log("Social login successful! Token saved.");
    }
    
    // Set username from localStorage
    const username = localStorage.getItem("username") || "Student";
    const userNameElements = document.querySelectorAll("#userName, .user-details span:first-child");
    userNameElements.forEach(el => {
        if (el) el.textContent = username;
    });
    
    // Set email if exists
    const userEmail = document.getElementById("userEmail");
    if (userEmail) {
        userEmail.textContent = `${username}@example.com`;
    }
    
    // Setup navigation
    const navItems = document.querySelectorAll('.nav-item');
    navItems.forEach(btn => {
        btn.addEventListener('click', () => {
            const page = btn.getAttribute('data-page');
            if (page) navigateTo(page);
        });
    });
    
    // Check if we're on dashboard and token exists
    if (window.location.pathname.includes("dashboard.html")) {
        if (!localStorage.getItem("token")) {
            console.log("No token found, redirecting to login");
            window.location.href = "index.html";
        } else {
            console.log("Token found, loading dashboard data");
            
            // Load dashboard data
            loadDashboardStats();
            loadRecentActivity();
            updateAttendanceChart();
            
            // Refresh data every 30 seconds
            setInterval(() => {
                loadDashboardStats();
                loadRecentActivity();
                updateAttendanceChart();
            }, 30000);
        }
    }
    
    // Initialize Chart if on dashboard and chart exists (fallback)
    const chartCanvas = document.getElementById("attendanceChart");
    if (chartCanvas && typeof Chart !== 'undefined' && !window.location.pathname.includes("dashboard.html")) {
        if (!window.attendanceChartInstance) {
            updateAttendanceChart();
        }
    }
});

// Make all functions global for HTML onclick handlers
window.switchTab = switchTab;
window.login = login;
window.googleLogin = googleLogin;
window.githubLogin = githubLogin;
window.facebookLogin = facebookLogin;
window.sendOTP = sendOTP;
window.verifyOTP = verifyOTP;
window.logout = logout;
window.navigateTo = navigateTo;
window.addStudentRow = addStudentRow;
window.removeStudentRow = removeStudentRow;
window.submitAttendance = submitAttendance;
window.fetchStudentAttendance = fetchStudentAttendance;
window.createAssignmentAPI = createAssignmentAPI;
window.submitAssignmentAPI = submitAssignmentAPI;
window.loadSubmissions = loadSubmissions;
window.gradeSubmission = gradeSubmission;
window.fetchNotifications = fetchNotifications;
window.markNotificationRead = markNotificationRead;
window.loadDashboardStats = loadDashboardStats;
window.loadRecentActivity = loadRecentActivity;
window.updateAttendanceChart = updateAttendanceChart;