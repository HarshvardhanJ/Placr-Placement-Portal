<template>
  <StudentLayout :show-search="false">
    <PageHeader
      title="Settings"
      subtitle="Adjust notifications and account preferences."
    >
      <template #actions>
        <div class="d-flex flex-wrap gap-2">
          <RouterLink to="/student/profile" class="btn btn-outline-primary">
            <i class="ti ti-id-badge-2 me-2"></i>Profile
          </RouterLink>
          <RouterLink to="/student" class="btn btn-primary">
            <i class="ti ti-layout-dashboard me-2"></i>Dashboard
          </RouterLink>
        </div>
      </template>
    </PageHeader>

    <div class="settings-shell">
      <div class="settings-hero card shadow-sm border-0 mb-4">
        <div
          class="card-body p-4 p-lg-5 d-flex flex-column flex-lg-row gap-4 align-items-lg-center justify-content-between"
        >
          <div>
            <span class="hero-kicker">Account Settings</span>
            <h3 class="fw-bold mb-2">Personalize your placement experience</h3>
            <p class="text-muted mb-0">
              Update notification preferences, privacy options, and account
              controls.
            </p>
          </div>

          <RouterLink to="/student/profile" class="btn btn-outline-primary">
            <i class="ti ti-user-edit me-2"></i>Edit Profile
          </RouterLink>
        </div>
      </div>

      <div class="row g-4">
        <div class="col-12 col-xl-8">
          <div class="card shadow-sm border-0">
            <div class="card-body p-4">
              <div
                class="d-flex align-items-start justify-content-between mb-4"
              >
                <div>
                  <h6 class="fw-semibold mb-1">Preferences</h6>
                  <small class="text-muted"
                    >Control how the portal works for you</small
                  >
                </div>
                <span class="pill-label">Student</span>
              </div>

              <div class="settings-list">
                <div
                  v-for="item in settings"
                  :key="item.key"
                  class="setting-item"
                >
                  <div class="d-flex align-items-start gap-3">
                    <div class="setting-icon">
                      <i :class="['ti', item.icon]"></i>
                    </div>
                    <div class="flex-grow-1">
                      <div class="fw-semibold">{{ item.label }}</div>
                      <small class="text-muted">{{ item.description }}</small>
                    </div>
                  </div>

                  <div class="form-check form-switch m-0">
                    <input
                      class="form-check-input"
                      type="checkbox"
                      :id="item.key"
                      v-model="item.enabled"
                    />
                  </div>
                </div>
              </div>

              <div class="d-flex flex-wrap gap-2 mt-4">
                <button type="button" class="btn btn-primary">
                  Save Settings
                </button>
                <button
                  type="button"
                  class="btn btn-outline-secondary"
                  @click="resetSettings"
                >
                  Reset
                </button>
              </div>
            </div>
          </div>
        </div>

        <div class="col-12 col-xl-4 d-flex flex-column gap-4">
          <div class="card shadow-sm border-0">
            <div class="card-body p-4">
              <h6 class="fw-semibold mb-3">Account status</h6>

              <div class="summary-stack">
                <div class="summary-item">
                  <div class="summary-label">Email alerts</div>
                  <div class="summary-value">
                    {{ emailAlertsEnabled ? "Enabled" : "Disabled" }}
                  </div>
                </div>
                <div class="summary-item">
                  <div class="summary-label">Resume</div>
                  <div class="summary-value">
                    {{ hasResume ? "Uploaded" : "Missing" }}
                  </div>
                </div>
              </div>
            </div>
          </div>

          <div class="card shadow-sm border-0">
            <div class="card-body p-4">
              <h6 class="fw-semibold mb-2">Need to change profile details?</h6>
              <p class="text-muted small mb-3">
                Edit your academic details, skills, and resume from the Profile
                page.
              </p>
              <div class="d-flex flex-wrap gap-2">
                <RouterLink
                  to="/student/profile"
                  class="btn btn-outline-primary btn-sm"
                >
                  Open Profile
                </RouterLink>
                <RouterLink
                  to="/student/drives"
                  class="btn btn-outline-secondary btn-sm"
                >
                  Browse Drives
                </RouterLink>
              </div>
            </div>
          </div>

          <div class="card shadow-sm border-0">
            <div class="card-body p-4">
              <h6 class="fw-semibold mb-2 text-danger">Danger zone</h6>
              <p class="text-muted small mb-3">
                Sign out safely when you are done using the portal.
              </p>
              <button
                type="button"
                class="btn btn-outline-danger btn-sm"
                @click="logout"
              >
                <i class="ti ti-logout me-2"></i>Log Out
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </StudentLayout>
</template>

<script setup>
import { computed, reactive, ref } from "vue";
import { useRouter } from "vue-router";
import { storeToRefs } from "pinia";
import StudentLayout from "@/layouts/StudentLayout.vue";
import PageHeader from "@/components/shared/PageHeader.vue";
import useAuthStore from "@/stores/authStore";
import { useStudentStore } from "@/stores/studentStore";

const router = useRouter();
const authStore = useAuthStore();
const studentStore = useStudentStore();
const { profile } = storeToRefs(studentStore);

const defaults = [
  {
    key: "emailAlerts",
    label: "Email alerts",
    description:
      "Get notified about interview schedules and placement updates.",
    icon: "ti-mail",
    enabled: true,
  },
  {
    key: "deadlineReminders",
    label: "Deadline reminders",
    description: "Receive reminders before application deadlines close.",
    icon: "ti-bell",
    enabled: true,
  },
  {
    key: "resumeSync",
    label: "Resume sync",
    description: "Keep your uploaded resume available for applications.",
    icon: "ti-file-upload",
    enabled: true,
  },
];

const settings = reactive(defaults.map((item) => ({ ...item })));

const emailAlertsEnabled = computed(
  () => settings.find((item) => item.key === "emailAlerts")?.enabled,
);

const profileVisibility = computed(() =>
  settings.find((item) => item.key === "profileVisibility")?.enabled
    ? "Visible"
    : "Hidden",
);

const hasResume = computed(() =>
  Boolean(
    profile.value?.resume_path ||
    profile.value?.resume_url ||
    profile.value?.resume,
  ),
);

const resetSettings = () => {
  settings.splice(0, settings.length, ...defaults.map((item) => ({ ...item })));
};

const logout = () => {
  if (!window.confirm("Are you sure you want to logout?")) return;
  authStore.logout();
  studentStore.clearStudentState();
  router.push("/login");
};
</script>

<style scoped>
.settings-shell {
  display: flex;
  flex-direction: column;
  gap: 1.25rem;
}

.settings-hero {
  border-radius: 1rem;
  background: linear-gradient(135deg, #ffffff 0%, #f8fbff 100%);
}

.hero-kicker {
  display: inline-flex;
  align-items: center;
  font-size: 0.78rem;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.08em;
  color: #0d6efd;
  margin-bottom: 0.35rem;
}

.pill-label {
  display: inline-flex;
  align-items: center;
  padding: 0.38rem 0.7rem;
  border-radius: 999px;
  background: #eef4ff;
  color: #0d6efd;
  font-size: 0.78rem;
  font-weight: 700;
}

.settings-list {
  display: flex;
  flex-direction: column;
  gap: 0.85rem;
}

.setting-item {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 1rem;
  padding: 1rem;
  border: 1px solid #e9ecef;
  border-radius: 16px;
  background: #fff;
}

.setting-icon {
  width: 42px;
  height: 42px;
  border-radius: 12px;
  background: #eef4ff;
  color: #0d6efd;
  display: grid;
  place-items: center;
  flex-shrink: 0;
  font-size: 1.05rem;
}

.summary-stack {
  display: flex;
  flex-direction: column;
  gap: 0.8rem;
}

.summary-item {
  padding: 0.9rem;
  border: 1px solid #e9ecef;
  border-radius: 14px;
  background: #fff;
}

.summary-label {
  font-size: 0.78rem;
  font-weight: 700;
  color: #6b7280;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  margin-bottom: 0.25rem;
}

.summary-value {
  font-weight: 700;
  color: #111827;
}
</style>
