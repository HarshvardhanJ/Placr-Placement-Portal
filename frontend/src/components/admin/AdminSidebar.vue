<template>
  <aside class="admin-sidebar">
    <div class="sidebar-brand">
      <div class="brand-text">
        <h4>PLACR</h4>
        <small>Admin Panel</small>
      </div>
    </div>

    <div class="sidebar-divider"></div>

    <nav class="sidebar-nav">
      <p class="sidebar-label">Navigation</p>

      <RouterLink
        to="/admin"
        class="sidebar-link"
        active-class="is-active"
        exact-active-class="is-active"
      >
        <i class="ti ti-layout-dashboard"></i>
        <span>Dashboard</span>
      </RouterLink>

      <RouterLink
        to="/admin/companies"
        class="sidebar-link"
        active-class="is-active"
        exact-active-class="is-active"
      >
        <i class="ti ti-building"></i>
        <span>Companies</span>
      </RouterLink>

      <RouterLink
        to="/admin/students"
        class="sidebar-link"
        active-class="is-active"
        exact-active-class="is-active"
      >
        <i class="ti ti-users"></i>
        <span>Students</span>
      </RouterLink>

      <RouterLink
        to="/admin/drives"
        class="sidebar-link"
        active-class="is-active"
        exact-active-class="is-active"
      >
        <i class="ti ti-briefcase"></i>
        <span>Drives</span>
      </RouterLink>

      <RouterLink
        to="/admin/applications"
        class="sidebar-link"
        active-class="is-active"
        exact-active-class="is-active"
      >
        <i class="ti ti-file-text"></i>
        <span>Applications</span>
      </RouterLink>
    </nav>

    <div class="sidebar-divider"></div>

    <div class="sidebar-stats">
      <p class="sidebar-label">Quick Status</p>

      <div class="stat-row">
        <span>Pending Companies</span>
        <span class="badge text-bg-warning">
          {{ stats.pending_companies }}
        </span>
      </div>

      <div class="stat-row">
        <span>Pending Drives</span>
        <span class="badge text-bg-info">
          {{ stats.pending_drives }}
        </span>
      </div>

      <div class="stat-row">
        <span>Blacklisted</span>
        <span class="badge text-bg-danger">
          {{ stats.blacklisted }}
        </span>
      </div>
    </div>

    <div class="sidebar-footer">
      <div class="admin-card">
        <div class="admin-avatar">
          <span>AD</span>
        </div>

        <div class="admin-meta">
          <div class="admin-name">Admin User</div>
          <small>Placement Cell</small>
        </div>
      </div>

      <div class="footer-actions">
        <button type="button" class="footer-link logout-btn" @click="logout">
          <i class="ti ti-logout"></i>
          <span>Logout</span>
        </button>
      </div>
    </div>
  </aside>
</template>

<script setup>
import { useRouter } from "vue-router";
import useAuthStore from "@/stores/authStore";
import { storeToRefs } from "pinia";
import { useAdminStore } from "@/stores/adminStore";

const adminStore = useAdminStore();
const router = useRouter();
const authStore = useAuthStore();
const { stats } = storeToRefs(adminStore);

const logout = () => {
  if (!window.confirm("Are you sure you want to logout?")) {
    return;
  }

  authStore.logout();
  router.push("/login");
};
</script>

<style scoped>
.admin-sidebar {
  width: 280px;
  min-height: 100vh;
  background: linear-gradient(180deg, #ffffff 0%, #f8fafc 100%);
  border-right: 1px solid #e9ecef;
  padding: 1.25rem;
  display: flex;
  flex-direction: column;
}

.sidebar-brand {
  display: flex;
  align-items: center;
  gap: 0.85rem;
  padding: 0.25rem 0.25rem 0.75rem;
}

.brand-mark {
  width: 42px;
  height: 42px;
  border-radius: 12px;
  background: linear-gradient(135deg, #0d6efd, #3b82f6);
  color: white;
  display: grid;
  place-items: center;
  font-weight: 700;
  letter-spacing: 0.5px;
  box-shadow: 0 8px 20px rgba(13, 110, 253, 0.22);
  flex-shrink: 0;
}

.brand-text h4 {
  margin: 0;
  font-weight: 800;
  line-height: 1;
  color: #1f2937;
}

.brand-text small {
  color: #6b7280;
  font-size: 0.85rem;
}

.sidebar-divider {
  height: 1px;
  background: #e9ecef;
  margin: 1rem 0;
}

.sidebar-nav,
.sidebar-stats {
  display: flex;
  flex-direction: column;
  gap: 0.35rem;
}

.sidebar-label {
  margin: 0 0 0.35rem;
  padding: 0 0.35rem;
  font-size: 0.72rem;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.08em;
  color: #94a3b8;
}

.sidebar-link,
.footer-link {
  width: 100%;
  border: 0;
  background: transparent;
  text-decoration: none;
  color: #4b5563;
  display: flex;
  align-items: center;
  gap: 0.9rem;
  padding: 0.9rem 1rem;
  border-radius: 14px;
  transition: all 0.2s ease;
  font-weight: 500;
  text-align: left;
}

.sidebar-link i,
.footer-link i {
  font-size: 1.15rem;
  flex-shrink: 0;
}

.sidebar-link:hover,
.footer-link:hover {
  background: #f1f5f9;
  color: #111827;
  transform: translateX(2px);
}

.sidebar-link.is-active {
  background: linear-gradient(135deg, #0d6efd, #2563eb);
  color: #fff;
  box-shadow: 0 12px 24px rgba(13, 110, 253, 0.18);
}

.sidebar-link.is-active i {
  color: #fff;
}

.sidebar-stats {
  margin-top: 0.25rem;
}

.stat-row {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 1rem;
  padding: 0.7rem 0.9rem;
  border-radius: 12px;
  background: #f8fafc;
  color: #374151;
  font-size: 0.92rem;
}

.sidebar-footer {
  margin-top: auto;
  padding-top: 1rem;
  display: flex;
  flex-direction: column;
  gap: 0.9rem;
}

.admin-card {
  display: flex;
  align-items: center;
  gap: 0.8rem;
  padding: 0.9rem;
  border-radius: 16px;
  background: #ffffff;
  border: 1px solid #e9ecef;
  box-shadow: 0 8px 18px rgba(15, 23, 42, 0.04);
}

.admin-avatar {
  width: 42px;
  height: 42px;
  border-radius: 50%;
  background: linear-gradient(135deg, #e0f2fe, #bfdbfe);
  color: #0d6efd;
  display: grid;
  place-items: center;
  font-weight: 700;
  font-size: 0.9rem;
  flex-shrink: 0;
}

.admin-meta {
  min-width: 0;
}

.admin-name {
  font-weight: 700;
  color: #111827;
  line-height: 1.2;
}

.admin-meta small {
  color: #6b7280;
}

.footer-actions {
  display: flex;
  flex-direction: column;
  gap: 0.35rem;
}

.logout-btn {
  cursor: pointer;
}

@media (max-width: 991.98px) {
  .admin-sidebar {
    width: 100%;
    min-height: auto;
  }
}
</style>
