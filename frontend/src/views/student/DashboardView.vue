<template>
  <StudentLayout v-model:search-query="searchQuery">
    <PageHeader
      title="Dashboard"
      subtitle="Track your eligible drives, applications, interviews, and offers."
    >
      <template #actions>
        <div class="d-flex flex-wrap gap-2">
          <RouterLink to="/student/drives" class="btn btn-primary">
            <i class="ti ti-briefcase me-2"></i>Browse Drives
          </RouterLink>
          <RouterLink to="/student/profile" class="btn btn-outline-primary">
            <i class="ti ti-user-edit me-2"></i>Complete Profile
          </RouterLink>
        </div>
      </template>
    </PageHeader>

    <div v-if="store.profileWarning" class="alert alert-warning d-flex align-items-center gap-2">
      <i class="ti ti-alert-triangle"></i>
      <span>Complete your profile (department, CGPA, year) to unlock eligible drives and applications.</span>
    </div>

    <div v-if="store.error" class="alert alert-danger">
      {{ store.error }}
    </div>

    <div class="tab-pills mb-4">
      <button
        v-for="tab in tabs"
        :key="tab.key"
        type="button"
        class="tab-pill"
        :class="{ active: activeTab === tab.key }"
        @click="activeTab = tab.key"
      >
        {{ tab.label }}
      </button>
    </div>

    <template v-if="activeTab === 'overview'">
      <div class="row g-3 mb-4">
        <div v-for="card in store.statsCards" :key="card.key" class="col-12 col-sm-6 col-xl-3">
          <StatCard :title="card.label" :value="card.value" :icon="card.icon" :delta="card.delta" />
        </div>
      </div>

      <div class="student-hero card shadow-sm border-0 mb-4">
        <div class="card-body p-4 p-lg-5 d-flex flex-column flex-lg-row gap-4 align-items-lg-center justify-content-between">
          <div class="hero-copy">
            <span class="hero-kicker">Welcome back</span>
            <h3 class="fw-bold mb-2">{{ studentName }}</h3>
            <p class="text-muted mb-0">
              Here is what is happening with your placements today.
            </p>
          </div>

          <div class="hero-actions d-flex flex-wrap gap-2">
            <RouterLink to="/student/applications" class="btn btn-outline-primary">
              View Applications
            </RouterLink>
            <RouterLink to="/student/interviews" class="btn btn-primary">
              Upcoming Interviews
            </RouterLink>
          </div>
        </div>
      </div>

      <div class="row g-4 align-items-start">
        <div class="col-12 col-xl-8">
          <StudentRecommendedDrives
            :drives="filteredEligibleDrives"
            :loading="store.loadingDashboard"
          />
        </div>

        <div class="col-12 col-xl-4 d-flex flex-column gap-4">
          <StudentUpcomingActions
            :upcoming-interviews="store.upcomingInterviews"
            :eligible-drives="filteredEligibleDrives"
          />
          <StudentActivityFeed
            :applications="store.appliedDrives"
            :shortlisted="store.shortlistedDrives"
            :selected="store.selectedDrives"
          />
        </div>
      </div>
    </template>

    <template v-else-if="activeTab === 'analytics'">
      <StudentAnalyticsPanel />
    </template>

    <template v-else>
      <StudentReportsPanel />
    </template>
  </StudentLayout>
</template>

<script setup>
import { computed, onMounted, ref, watch } from "vue";
import { storeToRefs } from "pinia";
import StudentLayout from "@/layouts/StudentLayout.vue";
import PageHeader from "@/components/shared/PageHeader.vue";
import StatCard from "@/components/shared/StatCard.vue";
import StudentRecommendedDrives from "@/components/student/StudentRecommendedDrives.vue";
import StudentUpcomingActions from "@/components/student/StudentUpcomingActions.vue";
import StudentActivityFeed from "@/components/student/StudentActivityFeed.vue";
import StudentAnalyticsPanel from "@/components/student/StudentAnalyticsPanel.vue";
import StudentReportsPanel from "@/components/student/StudentReportsPanel.vue";
import { useStudentStore } from "@/stores/studentStore";

const store = useStudentStore();
const { dashboard, profile } = storeToRefs(store);

const searchQuery = ref("");
const activeTab = ref("overview");

const tabs = [
  { key: "overview", label: "Overview" },
  { key: "analytics", label: "Analytics" },
  { key: "reports", label: "Reports" },
];

const studentName = computed(() => profile.value?.name || "Student");

const eligibleDrives = computed(() => dashboard.value?.eligible_drives || []);

const normalize = (value = "") => String(value).toLowerCase();

const filteredEligibleDrives = computed(() => {
  const query = normalize(searchQuery.value).trim();
  if (!query) return eligibleDrives.value;

  return eligibleDrives.value.filter((drive) => {
    const companyName = drive.company_name || drive.company?.name || "";
    const title = drive.job_title || "";
    const skills = drive.required_skills || drive.skills_required || "";
    return [companyName, title, skills].some((field) =>
      normalize(field).includes(query),
    );
  });
});

onMounted(async () => {
  await Promise.allSettled([
    store.fetchProfile(),
    store.fetchDashboard(),
  ]);
});

watch(
  () => searchQuery.value,
  async () => {
    if (activeTab.value !== "overview") return;
    // keep the UI responsive if the dashboard is already loaded; no extra request needed here
  },
);
</script>

<style scoped>
.tab-pills {
  display: inline-flex;
  gap: 0.25rem;
  padding: 0.35rem;
  border-radius: 16px;
  background: #eef2f7;
  border: 1px solid #e5e7eb;
}

.tab-pill {
  border: 0;
  background: transparent;
  color: #6b7280;
  font-weight: 700;
  padding: 0.7rem 1.1rem;
  border-radius: 12px;
  transition: all 0.2s ease;
}

.tab-pill.active {
  background: #fff;
  color: #0d6efd;
  box-shadow: 0 8px 20px rgba(15, 23, 42, 0.06);
}

.student-hero {
  border-radius: 1rem;
}

.hero-kicker {
  display: inline-flex;
  align-items: center;
  font-size: 0.8rem;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.08em;
  color: #0d6efd;
  margin-bottom: 0.35rem;
}

.hero-copy {
  min-width: 0;
}
</style>
