<template>
  <div class="dashboard-section">
    <div class="section-hero card shadow-sm border-0 mb-4">
      <div
        class="card-body p-4 p-lg-5 d-flex flex-column flex-lg-row gap-4 align-items-lg-center justify-content-between"
      >
        <div>
          <span class="hero-kicker">Reports</span>
          <h3 class="fw-bold mb-2">Your documents and placement records</h3>
          <p class="text-muted mb-0">
            Review resume status, application history, and placement
            confirmations.
          </p>
        </div>

        <button class="btn btn-primary" type="button" disabled>
          <i class="ti ti-download me-2"></i>Export CSV
        </button>
      </div>
    </div>

    <div class="row g-3 mb-4">
      <div
        v-for="card in reportCards"
        :key="card.label"
        class="col-12 col-md-4"
      >
        <div class="report-card card shadow-sm border-0 h-100">
          <div class="card-body p-4">
            <div class="d-flex align-items-start justify-content-between">
              <div>
                <div class="text-muted small mb-1">{{ card.label }}</div>
                <div
                  class="report-value"
                  :class="{ muted: card.value === 'Missing' }"
                >
                  {{ card.value }}
                </div>
              </div>
              <div class="report-badge">
                <i :class="['ti', card.icon]"></i>
              </div>
            </div>
            <small class="text-muted d-block mt-2">{{ card.caption }}</small>
          </div>
        </div>
      </div>
    </div>

    <div class="card shadow-sm border-0">
      <div class="card-body p-4">
        <div
          class="d-flex align-items-start justify-content-between gap-3 mb-4"
        >
          <div>
            <h6 class="fw-semibold mb-1">Quick actions</h6>
            <small class="text-muted"
              >Jump to the places you will use most often</small
            >
          </div>
          <span class="pill-label">Student</span>
        </div>

        <div class="d-flex flex-wrap gap-2">
          <RouterLink
            to="/student/profile"
            class="btn btn-outline-primary btn-sm"
          >
            Update Profile
          </RouterLink>
          <RouterLink
            to="/student/drives"
            class="btn btn-outline-secondary btn-sm"
          >
            View Drives
          </RouterLink>
          <RouterLink
            to="/student/applications"
            class="btn btn-outline-secondary btn-sm"
          >
            View Applications
          </RouterLink>
          <RouterLink
            to="/student/placements"
            class="btn btn-outline-secondary btn-sm"
          >
            View Placements
          </RouterLink>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed } from "vue";
import { storeToRefs } from "pinia";
import { useStudentStore } from "@/stores/studentStore";

const store = useStudentStore();
const { dashboard, profile } = storeToRefs(store);

const resumeStatus = computed(() => {
  const resume = profile.value?.resume_url || profile.value?.resume || "";
  return resume ? "Uploaded" : "Missing";
});

const reportCards = computed(() => [
  {
    label: "Resume",
    value: resumeStatus.value,
    caption: "Upload your resume PDF",
    icon: "ti-file-description",
  },
  {
    label: "Applications",
    value: Number(dashboard.value?.counts?.applied || 0),
    caption: "Tracked in your dashboard",
    icon: "ti-send",
  },
  {
    label: "Placements",
    value: Number(dashboard.value?.counts?.selected || 0),
    caption: "Offers or confirmations",
    icon: "ti-trophy",
  },
]);
</script>

<style scoped>
.dashboard-section {
  display: flex;
  flex-direction: column;
  gap: 1.25rem;
}

.section-hero {
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

.report-card {
  border-radius: 1rem;
  background: #fff;
}

.report-value {
  font-size: 2rem;
  font-weight: 800;
  color: #111827;
  line-height: 1.1;
}

.report-value.muted {
  color: #6b7280;
}

.report-badge {
  width: 38px;
  height: 38px;
  border-radius: 12px;
  background: #eef4ff;
  color: #0d6efd;
  display: grid;
  place-items: center;
  font-size: 1.1rem;
  flex-shrink: 0;
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
</style>
