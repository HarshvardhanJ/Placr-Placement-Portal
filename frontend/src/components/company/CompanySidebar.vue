<template>
  <aside class="company-sidebar">
    <div class="sidebar-brand">
      <div class="brand-text">
        <h4>PLACR</h4>
        <small>Placement Portal</small>
      </div>
    </div>

    <RouterLink
      to="/company/drives?new=1"
      class="btn btn-primary new-drive-btn"
    >
      <i class="ti ti-plus"></i>
      <span>New Job Drive</span>
    </RouterLink>

    <div class="sidebar-divider"></div>

    <nav class="sidebar-nav">
      <p class="sidebar-label">Navigation</p>

      <RouterLink
        v-for="item in navLinks"
        :key="item.to"
        :to="item.to"
        class="sidebar-link"
        active-class="is-active"
      >
        <i :class="['ti', item.icon]"></i>
        <span>{{ item.label }}</span>
      </RouterLink>
    </nav>

    <div class="sidebar-footer">
      <div class="company-card">
        <div class="company-avatar">{{ initials }}</div>
        <div class="company-meta">
          <div class="company-name">{{ companyName }}</div>
          <small>Company Account</small>
        </div>
      </div>

      <button type="button" class="footer-link logout-btn" @click="logout">
        <i class="ti ti-logout"></i>
        <span>Log Out</span>
      </button>
    </div>
  </aside>
</template>

<script setup>
import { computed } from "vue";
import { useRouter } from "vue-router";
import { storeToRefs } from "pinia";
import useAuthStore from "@/stores/authStore";
import { useCompanyStore } from "@/stores/companyStore";

const router = useRouter();
const authStore = useAuthStore();
const companyStore = useCompanyStore();
const { company } = storeToRefs(companyStore);

const navLinks = [
  { to: "/company", label: "Dashboard", icon: "ti-layout-dashboard" },
  { to: "/company/drives", label: "Jobs & Drives", icon: "ti-briefcase" },
  { to: "/company/applications", label: "Applications", icon: "ti-inbox" },
  { to: "/company/interviews", label: "Interviews", icon: "ti-calendar-event" },
  { to: "/company/placements", label: "Placements", icon: "ti-trophy" },
  { to: "/company/profile", label: "Profile", icon: "ti-id-badge-2" },
  { to: "/company/settings", label: "Settings", icon: "ti-settings" },
];

const companyName = computed(() => company.value?.name || "Company");

const initials = computed(
  () =>
    companyName.value
      .split(" ")
      .filter(Boolean)
      .slice(0, 2)
      .map((part) => part[0]?.toUpperCase())
      .join("") || "CO",
);

const logout = () => {
  if (!window.confirm("Are you sure you want to logout?")) {
    return;
  }
  authStore.logout();
  companyStore.clearCompanyState();
  router.push("/login");
};
</script>

<style scoped>
.company-sidebar {
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
  padding: 0.25rem 0.25rem 1rem;
}

.brand-mark {
  width: 42px;
  height: 42px;
  border-radius: 12px;
  background: linear-gradient(135deg, #0d6efd, #3b82f6);
  color: white;
  display: grid;
  place-items: center;
  font-size: 1.2rem;
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

.new-drive-btn {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
  border-radius: 12px;
  font-weight: 600;
  padding: 0.65rem 1rem;
  text-decoration: none;
}

.sidebar-divider {
  height: 1px;
  background: #e9ecef;
  margin: 1rem 0;
}

.sidebar-nav {
  display: flex;
  flex-direction: column;
  gap: 0.35rem;
  flex-grow: 1;
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
  padding: 0.85rem 1rem;
  border-radius: 14px;
  transition: all 0.2s ease;
  font-weight: 500;
  text-align: left;
  font-size: 0.95rem;
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

.sidebar-footer {
  margin-top: auto;
  padding-top: 1rem;
  display: flex;
  flex-direction: column;
  gap: 0.9rem;
}

.company-card {
  display: flex;
  align-items: center;
  gap: 0.8rem;
  padding: 0.9rem;
  border-radius: 16px;
  background: #ffffff;
  border: 1px solid #e9ecef;
  box-shadow: 0 8px 18px rgba(15, 23, 42, 0.04);
}

.company-avatar {
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

.company-meta {
  min-width: 0;
}

.company-name {
  font-weight: 700;
  color: #111827;
  line-height: 1.2;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.company-meta small {
  color: #6b7280;
}

.logout-btn {
  cursor: pointer;
}

@media (max-width: 991.98px) {
  .company-sidebar {
    width: 100%;
    min-height: auto;
  }
}
</style>
