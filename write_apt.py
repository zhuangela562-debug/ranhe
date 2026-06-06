# -*- coding: utf-8 -*-
import codecs

html = r"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>然合教育 - 预约管理</title>
<style>
* { margin:0; padding:0; box-sizing:border-box; }
body { font-family:'Microsoft YaHei',Arial,sans-serif; background:#F5F5F5; color:#333; }

.header { background:linear-gradient(135deg,#1D9E75 0%,#25b885 100%); color:white; padding:0 30px; height:60px; display:flex; align-items:center; justify-content:space-between; box-shadow:0 2px 10px rgba(0,0,0,0.1); position:fixed; top:0; left:0; right:0; z-index:100; }
.header h1 { font-size:20px; font-weight:600; display:flex; align-items:center; gap:8px; }
.logout-btn { background:rgba(255,255,255,0.2); border:1px solid rgba(255,255,255,0.3); color:white; padding:8px 15px; border-radius:5px; cursor:pointer; font-size:14px; font-family:inherit; }

.sidebar { width:250px; background:white; height:calc(100vh - 60px); position:fixed; top:60px; left:0; overflow-y:auto; box-shadow:2px 0 10px rgba(0,0,0,0.05); }
.menu-item { padding:15px 25px; display:flex; align-items:center; gap:12px; color:#666; text-decoration:none; border-left:3px solid transparent; transition:all 0.3s; }
.menu-item:hover { background:#f0f9f4; color:#1D9E75; border-left-color:#1D9E75; }
.menu-item.active { background:#f0f9f4; color:#1D9E75; border-left-color:#1D9E75; font-weight:600; }

.main-content { margin-left:250px; margin-top:60px; padding:30px; }
.page-title { font-size:24px; margin-bottom:10px; }
.page-subtitle { color:#666; margin-bottom:30px; font-size:14px; }

.toolbar { display:flex; justify-content:space-between; align-items:center; margin-bottom:20px; gap:15px; flex-wrap:wrap; }
.search-box { flex:1; max-width:400px; position:relative; }
.search-box input { width:100%; padding:10px 15px 10px 40px; border:2px solid #e0e0e0; border-radius:8px; font-size:14px; outline:none; font-family:inherit; }
.search-box input:focus { border-color:#1D9E75; }
.search-box::before { content:"🔍"; position:absolute; left:12px; top:50%; transform:translateY(-50%); font-size:16px; }

.btn-group { display:flex; gap:10px; }
.btn { padding:10px 20px; border:none; border-radius:8px; cursor:pointer; font-size:14px; font-weight:600; display:flex; align-items:center; gap:8px; transition:all 0.3s; font-family:inherit; }
.btn-primary { background:linear-gradient(135deg,#1D9E75 0%,#25b885 100%); color:white; }
.btn-primary:hover { transform:translateY(-2px); box-shadow:0 5px 15px rgba(29,158,117,0.3); }
.btn-secondary { background:white; color:#666; border:2px solid #e0e0e0; }
.btn-secondary:hover { background:#f9f9f9; border-color:#1D9E75; color:#1D9E75; }

.filter-tabs { display:flex; gap:10px; margin-bottom:20px; border-bottom:2px solid #e0e0e0; padding-bottom:10px; }
.filter-tab { padding:8px 16px; background:none; border:none; cursor:pointer; font-size:14px; color:#666; border-bottom:2px solid transparent; transition:all 0.3s; font-family:inherit; }
.filter-tab:hover { color:#1D9E75; }
.filter-tab.active { color:#1D9E75; border-bottom-color:#1D9E75; font-weight:600; }

.table-container { background:white; border-radius:10px; box-shadow:0 2px 10px rgba(0,0,0,0.05); overflow:hidden; }
.table { width:100%; border-collapse:collapse; }
.table th { text-align:left; padding:15px; background:#f9f9f9; color:#666; font-weight:600; font-size:14px; border-bottom:2px solid #eee; }
.table td { padding:15px; border-bottom:1px solid #eee; font-size:14px; }
.table tr:hover { background:#f9f9f9; }

.status-badge { display:inline-block; padding:5px 12px; border-radius:20px; font-size:12px; font-weight:600; }
.status-badge.pending { background:#FFF3E0; color:#FF9800; }
.status-badge.confirmed { background:#E8F5E9; color:#1D9E75; }
.status-badge.cancelled { background:#FFEBEE; color:#f44336; }
.status-badge.completed { background:#E3F2FD; color:#2196F3; }

.action-buttons { display:flex; gap:8px; }
.action-btn { padding:5px 10px; border:none; border-radius:5px; cursor:pointer; font-size:12px; transition:all 0.3s; font-family:inherit; }
.action-btn.view { background:#E3F2FD; color:#2196F3; }
.action-btn.view:hover { background:#2196F3; color:white; }
.action-btn.edit { background:#FFF3E0; color:#FF9800; }
.action-btn.edit:hover { background:#FF9800; color:white; }
.action-btn.delete { background:#FFEBEE; color:#f44336; }
.action-btn.delete:hover { background:#f44336; color:white; }

.pagination { display:flex; justify-content:center; align-items:center; gap:10px; margin-top:20px; }
.pagination button { padding:8px 12px; border:1px solid #e0e0e0; background:white; cursor:pointer; border-radius:5px; transition:all 0.3s; font-family:inherit; }
.pagination button:hover { background:#f9f9f9; border-color:#1D9E75; color:#1D9E75; }
.pagination button.active { background:#1D9E75; color:white; border-color:#1D9E75; }
.pagination span { color:#666; font-size:14px; }

/* 模态框 */
.modal-mask {
    display:none;
    position:fixed; top:0; left:0;
    width:100%; height:100%;
    background:rgba(0,0,0,0.5);
    z-index:2000;
}
.modal-mask.show {
    display:flex !important;
    justify-content:center;
    align-items:center;
}
.modal-box {
    background:white; border-radius:10px;
    width:90%; max-width:600px;
    max-height:90vh; overflow-y:auto;
    box-shadow:0 10px 30px rgba(0,0,0,0.3);
    animation:modalIn 0.3s ease;
}
@keyframes modalIn { from{opacity:0;transform:translateY(-50px);} to{opacity:1;transform:translateY(0);} }
.modal-header { padding:20px 30px; border-bottom:1px solid #eee; display:flex; justify-content:space-between; align-items:center; }
.modal-header h3 { font-size:18px; }
.modal-close { background:none; border:none; font-size:24px; cursor:pointer; color:#999; padding:0 5px; font-family:inherit; }
.modal-close:hover { color:#333; }
.modal-body { padding:30px; }
.modal-footer { padding:20px 30px; border-top:1px solid #eee; display:flex; justify-content:flex-end; gap:10px; }

.form-group { margin-bottom:20px; }
.form-group label { display:block; margin-bottom:8px; font-weight:500; font-size:14px; }
.form-group input,
.form-group select,
.form-group textarea {
    width:100%; padding:10px 15px;
    border:2px solid #e0e0e0; border-radius:8px;
    font-size:14px; outline:none; font-family:inherit;
}
.form-group input:focus,
.form-group select:focus,
.form-group textarea:focus { border-color:#1D9E75; }
.form-group textarea { resize:vertical; min-height:100px; }
</style>
</head>
<body>

<div class="header">
    <h1>
        <img src="logo.png" alt="然合教育" style="height:36px;width:36px;vertical-align:middle;margin-right:8px;border-radius:50%;object-fit:cover;">
        然合教育预约系统
    </h1>
    <div>
        <span style="margin-right:15px;">欢迎，管理员</span>
        <button class="logout-btn" onclick="logout()">退出登录</button>
    </div>
</div>

<div class="sidebar">
    <a href="dashboard.html" class="menu-item"><span>📊</span><span>仪表板</span></a>
    <a href="appointments.html" class="menu-item active"><span>📅</span><span>预约管理</span></a>
    <a href="students.html" class="menu-item"><span>👨‍👩‍👧‍👦</span><span>学生管理</span></a>
    <a href="teachers.html" class="menu-item"><span>👩‍🏫</span><span>教师管理</span></a>
    <a href="courses.html" class="menu-item"><span>📚</span><span>课程管理</span></a>
    <a href="reports.html" class="menu-item"><span>📈</span><span>报表统计</span></a>
    <a href="settings.html" class="menu-item"><span>⚙️</span><span>系统设置</span></a>
</div>

<div class="main-content">
    <h2 class="page-title">预约管理</h2>
    <p class="page-subtitle">管理所有学生的预约信息</p>

    <div class="toolbar">
        <div class="search-box">
            <input type="text" placeholder="搜索学生姓名、课程..." id="searchInput">
        </div>
        <div class="btn-group">
            <button class="btn btn-primary" onclick="openModal('add')">➕ 新增预约</button>
            <button class="btn btn-secondary">📊 导出数据</button>
        </div>
    </div>

    <div class="filter-tabs">
        <button class="filter-tab active" onclick="filterByStatus('all',this)">全部</button>
        <button class="filter-tab" onclick="filterByStatus('pending',this)">待确认</button>
        <button class="filter-tab" onclick="filterByStatus('confirmed',this)">已确认</button>
        <button class="filter-tab" onclick="filterByStatus('completed',this)">已完成</button>
        <button class="filter-tab" onclick="filterByStatus('cancelled',this)">已取消</button>
    </div>

    <div class="table-container">
        <table class="table">
            <thead>
                <tr>
                    <th>预约编号</th><th>学生姓名</th><th>课程类型</th>
                    <th>教师</th><th>预约时间</th><th>来源</th>
                    <th>状态</th><th>操作</th>
                </tr>
            </thead>
            <tbody id="apptTable">
                <tr data-status="pending">
                    <td>#AP20260606001</td><td>张三</td><td>ABA训练</td>
                    <td>李老师</td><td>2026-06-06 09:00</td><td>大众点评</td>
                    <td><span class="status-badge pending">待确认</span></td>
                    <td>
                        <div class="action-buttons">
                            <button class="action-btn view" onclick="openModal('view',1)">查看</button>
                            <button class="action-btn edit" onclick="openModal('edit',1)">编辑</button>
                            <button class="action-btn delete" onclick="deleteAppt(1)">删除</button>
                        </div>
                    </td>
                </tr>
                <tr data-status="confirmed">
                    <td>#AP20260606002</td><td>李四</td><td>NET自然情境教学</td>
                    <td>王老师</td><td>2026-06-06 10:00</td><td>残联</td>
                    <td><span class="status-badge confirmed">已确认</span></td>
                    <td>
                        <div class="action-buttons">
                            <button class="action-btn view" onclick="openModal('view',2)">查看</button>
                            <button class="action-btn edit" onclick="openModal('edit',2)">编辑</button>
                            <button class="action-btn delete" onclick="deleteAppt(2)">删除</button>
                        </div>
                    </td>
                </tr>
            </tbody>
        </table>
    </div>

    <div class="pagination">
        <button onclick="changePage(-1)">上一页</button>
        <button class="active" onclick="goPage(1)">1</button>
        <button onclick="goPage(2)">2</button>
        <button onclick="goPage(3)">3</button>
        <span>...</span>
        <button onclick="goPage(10)">10</button>
        <button onclick="changePage(1)">下一页</button>
    </div>
</div>

<!-- 模态框 -->
<div class="modal-mask" id="modalMask">
    <div class="modal-box">
        <div class="modal-header">
            <h3 id="modalTitle">新增预约</h3>
            <button class="modal-close" onclick="closeModal()">×</button>
        </div>
        <div class="modal-body">
            <div class="form-group">
                <label>学生姓名</label>
                <input type="text" id="f_student" required>
            </div>
            <div class="form-group">
                <label>课程类型</label>
                <select id="f_course" required>
                    <option value="">请选择</option>
                    <option>ABA训练</option>
                    <option>NET自然情境教学</option>
                    <option>言语治疗</option>
                    <option>感统训练</option>
                    <option>社交技能训练</option>
                </select>
            </div>
            <div class="form-group">
                <label>教师</label>
                <select id="f_teacher" required>
                    <option value="">请选择</option>
                    <option>李老师</option>
                    <option>王老师</option>
                    <option>张老师</option>
                    <option>刘老师</option>
                </select>
            </div>
            <div class="form-group">
                <label>预约日期</label>
                <input type="date" id="f_date" required>
            </div>
            <div class="form-group">
                <label>预约时间</label>
                <input type="time" id="f_time" required>
            </div>
            <div class="form-group">
                <label>用户来源</label>
                <select id="f_source" onchange="onSourceChange()" required>
                    <option value="">请选择</option>
                    <option value="大众点评">大众点评</option>
                    <option value="高德">高德</option>
                    <option value="残联">残联</option>
                    <option value="抖音">抖音</option>
                    <option value="公众号">公众号</option>
                    <option value="__custom__">自定义</option>
                </select>
            </div>
            <div class="form-group" id="f_customGroup" style="display:none;">
                <label>自定义来源</label>
                <input type="text" id="f_customSource" placeholder="请输入来源名称">
            </div>
            <div class="form-group">
                <label>备注</label>
                <textarea id="f_notes" placeholder="请输入备注..."></textarea>
            </div>
        </div>
        <div class="modal-footer">
            <button class="btn btn-secondary" onclick="closeModal()">取 消</button>
            <button class="btn btn-primary" onclick="saveAppt()">保 存</button>
        </div>
    </div>
</div>

<script>
/* ===== 搜索 ===== */
var searchInput = document.getElementById('searchInput');
if (searchInput) {
    searchInput.addEventListener('input', function() {
        var term = this.value.toLowerCase();
        var rows = document.querySelectorAll('#apptTable tr');
        for (var i = 0; i < rows.length; i++) {
            rows[i].style.display = rows[i].textContent.toLowerCase().indexOf(term) !== -1 ? '' : 'none';
        }
    });
}

/* ===== 按状态筛选 ===== */
function filterByStatus(status, btn) {
    var tabs = document.querySelectorAll('.filter-tab');
    for (var i = 0; i < tabs.length; i++) {
        tabs[i].classList.remove('active');
    }
    if (btn) btn.classList.add('active');
    var rows = document.querySelectorAll('#apptTable tr');
    for (var i = 0; i < rows.length; i++) {
        if (status === 'all') {
            rows[i].style.display = '';
        } else {
            rows[i].style.display = rows[i].getAttribute('data-status') === status ? '' : 'none';
        }
    }
}

/* ===== 打开模态框 ===== */
function openModal(mode, id) {
    var mask = document.getElementById('modalMask');
    if (!mask) { alert('页面未就绪'); return; }
    var title = document.getElementById('modalTitle');
    if (mode === 'add') {
        title.textContent = '新增预约';
        clearForm();
    } else if (mode === 'view') {
        title.textContent = '查看预约';
        fillDemo(id);
    } else if (mode === 'edit') {
        title.textContent = '编辑预约';
        fillDemo(id);
    }
    mask.classList.add('show');
}

/* ===== 关闭模态框 ===== */
function closeModal() {
    var mask = document.getElementById('modalMask');
    if (mask) mask.classList.remove('show');
}

/* ===== 点击遮罩关闭 ===== */
(function(){
    var m = document.getElementById('modalMask');
    if (m) {
        m.addEventListener('click', function(e){
            if (e.target === this) closeModal();
        });
    }
})();

/* ===== 来源切换 ===== */
function onSourceChange() {
    var sel = document.getElementById('f_source');
    var grp = document.getElementById('f_customGroup');
    if (sel.value === '__custom__') {
        grp.style.display = '';
    } else {
        grp.style.display = 'none';
    }
}

/* ===== 清空表单 ===== */
function clearForm() {
    var ids = ['f_student','f_course','f_teacher','f_date','f_time','f_source','f_customSource','f_notes'];
    for (var i = 0; i < ids.length; i++) {
        var el = document.getElementById(ids[i]);
        if (el) el.value = '';
    }
    var g = document.getElementById('f_customGroup');
    if (g) g.style.display = 'none';
}

/* ===== 填入演示数据 ===== */
function fillDemo(id) {
    document.getElementById('f_student').value = id === 1 ? '张三' : '李四';
    document.getElementById('f_course').value = id === 1 ? 'ABA训练' : 'NET自然情境教学';
    document.getElementById('f_teacher').value = id === 1 ? '李老师' : '王老师';
    document.getElementById('f_date').value = '2026-06-06';
    document.getElementById('f_time').value = id === 1 ? '09:00' : '10:00';
    document.getElementById('f_source').value = id === 1 ? '大众点评' : '残联';
    var g = document.getElementById('f_customGroup');
    if (g) g.style.display = 'none';
    document.getElementById('f_notes').value = '';
}

/* ===== 保存 ===== */
function saveAppt() {
    var ok = true;
    var reqIds = ['f_student','f_course','f_teacher','f_date','f_time','f_source'];
    for (var i = 0; i < reqIds.length; i++) {
        var el = document.getElementById(reqIds[i]);
        if (!el || !el.value) { ok = false; break; }
    }
    if (!ok) { alert('请填写所有必填项！'); return; }
    var src = document.getElementById('f_source').value;
    if (src === '__custom__') {
        var cs = document.getElementById('f_customSource').value;
        if (!cs) { alert('请输入自定义来源！'); return; }
    }
    alert('保存成功！（演示模式）');
    closeModal();
}

/* ===== 删除 ===== */
function deleteAppt(id) {
    if (confirm('确定删除这条预约记录？')) {
        alert('删除成功！（演示模式）');
    }
}

/* ===== 退出登录 ===== */
function logout() {
    if (confirm('确定退出登录？')) window.location.href = 'login.html';
}

/* ===== 分页 ===== */
var currentPage = 1;
var maxPage = 10;
function changePage(dir) {
    currentPage = Math.max(1, Math.min(maxPage, currentPage + dir));
    refreshPageBtns();
}
function goPage(n) {
    currentPage = n;
    refreshPageBtns();
}
function refreshPageBtns() {
    var btns = document.querySelectorAll('.pagination button');
    for (var i = 0; i < btns.length; i++) {
        btns[i].classList.remove('active');
        var num = parseInt(btns[i].textContent);
        if (!isNaN(num) && num === currentPage) {
            btns[i].classList.add('active');
        }
    }
}
</script>
</body>
</html>"""

with codecs.open(r"F:\26特殊教育\预约系统升级\deploy\appointments.html", "w", "utf-8") as f:
    f.write(html)

print("写入完成")
