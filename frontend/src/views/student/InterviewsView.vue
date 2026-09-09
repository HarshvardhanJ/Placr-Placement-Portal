<template>
  <StudentLayout v-model:search-query="searchQuery">
    <PageHeader
      title="Interviews"
      subtitle="See upcoming interview schedules and feedback."
    >
      <template #actions>
        <div class="d-flex flex-wrap gap-2">
          <RouterLink
            to="/student/applications"
            class="btn btn-outline-primary"
          >
            <i class="ti ti-file-text me-2"></i>Applications
          </RouterLink>
          <RouterLink to="/student/placements" class="btn btn-primary">
            <i class="ti ti-trophy me-2"></i>Placements
          </RouterLink>
        </div>
      </template>
    </PageHeader>

    <div
      v-if="store.profileWarning"
      class="alert alert-warning d-flex align-items-center gap-2"
    >
      <i class="ti ti-alert-triangle"></i>
      <span
        >Complete your profile to unlock full interview and placement
        visibility.</span
      >
    </div>

    <div v-if="store.error" class="alert alert-danger">
      {{ store.error }}
    </div>

    <div class="interviews-shell">
      <div class="interviews-hero card shadow-sm border-0 mb-4">
        <div
          class="card-body p-4 p-lg-5 d-flex flex-column flex-lg-row gap-4 align-items-lg-center justify-content-between"
        >
          <div>
            <span class="hero-kicker">Interviews</span>
            <h3 class="fw-bold mb-2">Track rounds, timings, and feedback</h3>
            <p class="text-muted mb-0">
              Keep an eye on upcoming interviews, review round details, and
              follow placement progress.
            </p>
          </div>

          <div class="d-flex flex-wrap gap-2">
            <RouterLink to="/student/drives" class="btn btn-outline-primary">
              <i class="ti ti-briefcase me-2"></i>Browse Drives
            </RouterLink>
            <RouterLink to="/student/profile" class="btn btn-primary">
              <i class="ti ti-user-edit me-2"></i>Update Profile
            </RouterLink>
          </div>
        </div>
      </div>

      <div class="row g-3 mb-4">
        <div
          v-for="card in statsCards"
          :key="card.label"
          class="col-12 col-sm-6 col-xl-3"
        >
          <StatCard
            :title="card.label"
            :value="card.value"
            :icon="card.icon"
            :delta="card.delta"
          />
        </div>
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
          <span class="pill-count">{{ tab.count }}</span>
        </button>
      </div>

      <div class="row g-4 align-items-start">
        <div class="col-12 col-xl-8">
          <div class="card shadow-sm border-0">
            <div class="card-body p-4">
              <div
                class="d-flex flex-column flex-lg-row gap-3 justify-content-between align-items-lg-center mb-4"
              >
                <div>
                  <h6 class="fw-semibold mb-1">Interview schedule</h6>
                  <small class="text-muted">
                    {{ filteredInterviews.length }} round{{
                      filteredInterviews.length === 1 ? "" : "s"
                    }}
                    shown
                  </small>
                </div>

                <div class="d-flex flex-wrap gap-2">
                  <select
                    v-model="sortBy"
                    class="form-select form-select-sm sort-select"
                  >
                    <option value="soonest">Sort by soonest</option>
                    <option value="company">Sort by company</option>
                    <option value="role">Sort by role</option>
                    <option value="latest">Sort by latest</option>
                  </select>
                </div>
              </div>

              <div class="interview-list">
                <div
                  v-for="item in filteredInterviews"
                  :key="item.interviewKey"
                  class="interview-card"
                >
                  <div
                    class="d-flex flex-column flex-lg-row gap-3 justify-content-between"
                  >
                    <div class="d-flex gap-3">
                      <div class="company-logo">
                        {{ item.companyInitials }}
                      </div>

                      <div>
                        <div
                          class="d-flex flex-wrap align-items-center gap-2 mb-1"
                        >
                          <h5 class="mb-0 fw-semibold">{{ item.job_title }}</h5>
                          <span
                            class="status-badge"
                            :class="statusClass(item.status)"
                          >
                            {{ statusLabel(item.status) }}
                          </span>
                        </div>

                        <div
                          class="text-muted small d-flex flex-wrap align-items-center gap-2"
                        >
                          <span>{{ item.company }}</span>
                          <span v-if="item.interview_type"
                            >• {{ item.interview_type }}</span
                          >
                          <span v-if="item.interview_date"
                            >• {{ formatDate(item.interview_date) }}</span
                          >
                        </div>

                        <div v-if="item.remarks" class="feedback-box mt-3">
                          <div class="feedback-label">Feedback / Remarks</div>
                          <div class="feedback-text">{{ item.remarks }}</div>
                        </div>
                      </div>
                    </div>

                    <div class="text-lg-end">
                      <div class="small text-muted mb-1">Round date</div>
                      <div class="fw-semibold">{{ item.interviewLabel }}</div>
                      <div class="small text-muted mt-1">
                        {{ item.roundHint }}
                      </div>
                    </div>
                  </div>

                  <div
                    class="application-footer mt-3 pt-3 border-top d-flex flex-wrap justify-content-between align-items-center gap-2"
                  >
                    <div class="small text-muted">
                      {{ item.followupLabel }}
                    </div>

                    <div class="d-flex flex-wrap gap-2">
                      <RouterLink
                        to="/student/applications"
                        class="btn btn-outline-primary btn-sm"
                      >
                        View Application
                      </RouterLink>
                      <RouterLink
                        to="/student/placements"
                        class="btn btn-primary btn-sm"
                      >
                        Placements
                      </RouterLink>
                    </div>
                  </div>
                </div>
              </div>

              <div v-if="!filteredInterviews.length" class="empty-wrap mt-4">
                <div class="empty-state">
                  <i class="ti ti-calendar-off empty-icon"></i>
                  <div class="fw-semibold mb-1">No interviews found</div>
                  <small class="text-muted d-block mb-3">
                    Interviews will appear here after you are shortlisted.
                  </small>
                  <div class="d-flex flex-wrap justify-content-center gap-2">
                    <button
                      type="button"
                      class="btn btn-outline-primary btn-sm"
                      @click="resetFilters"
                    >
                      Clear Filters
                    </button>
                    <RouterLink
                      to="/student/drives"
                      class="btn btn-primary btn-sm"
                    >
                      Browse Drives
                    </RouterLink>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>

        <div class="col-12 col-xl-4 d-flex flex-column gap-4">
          <div class="card shadow-sm border-0">
            <div class="card-body p-4">
              <div
                class="d-flex align-items-start justify-content-between mb-3"
              >
                <div>
                  <h6 class="fw-semibold mb-1">Quick filters</h6>
                  <small class="text-muted"
                    >Jump between interview states</small
                  >
                </div>
                <i class="ti ti-adjustments-horizontal text-primary"></i>
              </div>

              <div class="filter-stack">
                <button
                  v-for="filter in filterChips"
                  :key="filter.key"
                  type="button"
                  class="filter-chip"
                  :class="{ active: activeTab === filter.key }"
                  @click="activeTab = filter.key"
                >
                  {{ filter.label }}
                  <span class="chip-count">{{ filter.count }}</span>
                </button>
              </div>
            </div>
          </div>

          <div class="card shadow-sm border-0">
            <div class="card-body p-4">
              <div
                class="d-flex align-items-start justify-content-between mb-3"
              >
                <div>
                  <h6 class="fw-semibold mb-1">Upcoming round</h6>
                  <small class="text-muted">Next scheduled interview</small>
                </div>
                <i class="ti ti-clock text-primary"></i>
              </div>

              <div v-if="nextInterview" class="deadline-item">
                <div class="fw-semibold">{{ nextInterview.job_title }}</div>
                <small class="text-muted d-block">{{
                  nextInterview.company
                }}</small>
                <div class="mt-3">
                  <span class="deadline-badge">{{
                    nextInterview.interviewLabel
                  }}</span>
                </div>
              </div>

              <div v-else class="sidebar-empty">
                <i class="ti ti-calendar-off sidebar-empty-icon"></i>
                <div class="fw-semibold">No upcoming interviews</div>
                <small class="text-muted"
                  >Shortlisted rounds will show up here.</small
                >
              </div>
            </div>
          </div>

          <div class="card shadow-sm border-0">
            <div class="card-body p-4">
              <h6 class="fw-semibold mb-2">Interview prep</h6>
              <p class="text-muted small mb-3">
                Review the JD, practice common questions, and keep your resume
                handy.
              </p>
              <div class="d-flex flex-wrap gap-2">
                <RouterLink
                  to="/student/profile"
                  class="btn btn-outline-primary btn-sm"
                >
                  Review Profile
                </RouterLink>
                <RouterLink
                  to="/student/applications"
                  class="btn btn-outline-secondary btn-sm"
                >
                  Application History
                </RouterLink>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </StudentLayout>
</template>

<script setup>
import { computed, onMounted, ref } from "vue";
import { storeToRefs } from "pinia";
import StudentLayout from "@/layouts/StudentLayout.vue";
import PageHeader from "@/components/shared/PageHeader.vue";
import StatCard from "@/components/shared/StatCard.vue";
import { useStudentStore } from "@/stores/studentStore";

const store = useStudentStore();
const { dashboard } = storeToRefs(store);

const searchQuery = ref("");
const activeTab = ref("all");
const sortBy = ref("soonest");

const normalize = (value = "") => String(value).toLowerCase().trim();

const flattenInterview = (source, status) => {
  const drive = source?.drive || source || {};
  return {
    interviewKey:
      source.application_id ||
      drive.drive_id ||
      `${status}-${drive.job_title || "interview"}`,
    application_id: source.application_id || null,
    drive_id: drive.drive_id || null,
    status,
    job_title: drive.job_title || "Drive",
    company:
      source.company || drive.company?.name || drive.company_name || "Company",
    interview_type: source.interview_type || "",
    interview_date: source.interview_date || null,
    remarks: source.remarks || "",
    drive,
  };
};

const interviews = computed(() => {
  const list = [];

  for (const item of dashboard.value?.upcoming_interviews || []) {
    list.push(flattenInterview(item, "upcoming"));
  }

  for (const item of dashboard.value?.shortlisted_drives || []) {
    list.push(flattenInterview(item, "shortlisted"));
  }

  for (const item of dashboard.value?.selected_drives || []) {
    list.push(flattenInterview(item, "selected"));
  }

  const byKey = new Map();
  const priority = { upcoming: 3, shortlisted: 2, selected: 1 };

  for (const item of list) {
    const existing = byKey.get(item.interviewKey);
    if (!existing || priority[item.status] > priority[existing.status]) {
      byKey.set(item.interviewKey, item);
    }
  }

  return [...byKey.values()];
});

const statsCards = computed(() => [
  {
    label: "Upcoming",
    value: interviews.value.filter((i) => i.status === "upcoming").length,
    delta: "Scheduled rounds",
    icon: "ti-calendar-event",
  },
  {
    label: "Shortlisted",
    value: interviews.value.filter((i) => i.status === "shortlisted").length,
    delta: "Waiting on interview",
    icon: "ti-star",
  },
  {
    label: "Selected",
    value: interviews.value.filter((i) => i.status === "selected").length,
    delta: "Offer stage",
    icon: "ti-trophy",
  },
  {
    label: "Total",
    value: interviews.value.length,
    delta: "Tracked rounds",
    icon: "ti-list-check",
  },
]);

const tabs = computed(() => [
  { key: "all", label: "All", count: interviews.value.length },
  {
    key: "upcoming",
    label: "Upcoming",
    count: interviews.value.filter((i) => i.status === "upcoming").length,
  },
  {
    key: "shortlisted",
    label: "Shortlisted",
    count: interviews.value.filter((i) => i.status === "shortlisted").length,
  },
  {
    key: "selected",
    label: "Selected",
    count: interviews.value.filter((i) => i.status === "selected").length,
  },
]);

const filterChips = tabs;

const formatDate = (value) => {
  if (!value) return "";
  const date = new Date(value);
  if (Number.isNaN(date.getTime())) return String(value);
  return date.toLocaleDateString("en-GB", {
    day: "numeric",
    month: "short",
    year: "numeric",
  });
};

const filteredInterviews = computed(() => {
  let items = [...interviews.value];

  if (activeTab.value !== "all") {
    items = items.filter((item) => item.status === activeTab.value);
  }

  const query = normalize(searchQuery.value);
  if (query) {
    items = items.filter((item) => {
      const fields = [
        item.job_title,
        item.company,
        item.interview_type,
        item.remarks,
      ];
      return fields.some((field) => normalize(field).includes(query));
    });
  }

  items.sort((a, b) => {
    if (sortBy.value === "company") {
      return normalize(a.company).localeCompare(normalize(b.company));
    }

    if (sortBy.value === "role") {
      return normalize(a.job_title).localeCompare(normalize(b.job_title));
    }

    if (sortBy.value === "latest") {
      return (
        new Date(b.interview_date || 0).getTime() -
        new Date(a.interview_date || 0).getTime()
      );
    }

    return (
      new Date(a.interview_date || 0).getTime() -
      new Date(b.interview_date || 0).getTime()
    );
  });

  return items.map((item) => ({
    ...item,
    companyInitials:
      item.company
        .split(" ")
        .filter(Boolean)
        .slice(0, 2)
        .map((part) => part[0]?.toUpperCase())
        .join("") || "CO",
    interviewLabel: item.interview_date
      ? formatDate(item.interview_date)
      : "TBA",
    roundHint: item.interview_type || "Round details pending",
    followupLabel: item.remarks
      ? "Feedback added by company"
      : "No feedback shared yet",
  }));
});

const nextInterview = computed(
  () =>
    [...filteredInterviews.value]
      .filter((item) => item.interview_date)
      .sort(
        (a, b) => new Date(a.interview_date) - new Date(b.interview_date),
      )[0] || null,
);

const statusLabel = (status) => {
  if (status === "upcoming") return "Upcoming";
  if (status === "shortlisted") return "Shortlisted";
  if (status === "selected") return "Selected";
  return "Scheduled";
};

const statusClass = (status) => {
  if (status === "upcoming") return "status-upcoming";
  if (status === "shortlisted") return "status-shortlisted";
  if (status === "selected") return "status-selected";
  return "status-muted";
};

const resetFilters = () => {
  activeTab.value = "all";
  sortBy.value = "soonest";
  searchQuery.value = "";
};

onMounted(async () => {
  await Promise.allSettled([store.fetchProfile?.(), store.fetchDashboard?.()]);
});
</script>

<style scoped>
.interviews-shell {
  display: flex;
  flex-direction: column;
  gap: 1.25rem;
}

.interviews-hero {
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
  display: inline-flex;
  align-items: center;
  gap: 0.45rem;
}

.tab-pill.active {
  background: #fff;
  color: #0d6efd;
  box-shadow: 0 8px 20px rgba(15, 23, 42, 0.06);
}

.pill-count {
  min-width: 1.6rem;
  padding: 0.15rem 0.4rem;
  border-radius: 999px;
  background: #f1f5f9;
  color: #6b7280;
  font-size: 0.72rem;
  text-align: center;
}

.tab-pill.active .pill-count {
  background: #eef4ff;
  color: #0d6efd;
}

.sort-select {
  min-width: 180px;
}

.interview-list {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.interview-card {
  border: 1px solid #e9ecef;
  border-radius: 1rem;
  background: #fff;
  padding: 1rem;
  box-shadow: 0 8px 18px rgba(15, 23, 42, 0.03);
}

.company-logo {
  width: 56px;
  height: 56px;
  border-radius: 16px;
  background: linear-gradient(135deg, #eef4ff, #dbeafe);
  color: #0d6efd;
  display: grid;
  place-items: center;
  font-weight: 800;
  flex-shrink: 0;
}

.status-badge {
  display: inline-flex;
  align-items: center;
  padding: 0.3rem 0.6rem;
  border-radius: 999px;
  font-size: 0.78rem;
  font-weight: 700;
}

.status-upcoming {
  background: #eef4ff;
  color: #0d6efd;
}

.status-shortlisted {
  background: #fff7e6;
  color: #b45309;
}

.status-selected {
  background: #e8f8ef;
  color: #047857;
}

.status-muted {
  background: #f1f5f9;
  color: #64748b;
}

.feedback-box {
  padding: 0.85rem 0.95rem;
  border-radius: 14px;
  background: #f8fbff;
  border: 1px solid #e6eefb;
}

.feedback-label {
  font-size: 0.78rem;
  font-weight: 700;
  color: #0d6efd;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  margin-bottom: 0.25rem;
}

.feedback-text {
  color: #374151;
  font-size: 0.92rem;
}

.application-footer {
  gap: 0.75rem;
}

.empty-wrap {
  display: flex;
  justify-content: center;
}

.empty-state {
  width: 100%;
  max-width: 620px;
  min-height: 280px;
  display: grid;
  place-items: center;
  text-align: center;
  padding: 2rem 1rem;
  border: 1px dashed #d9dee7;
  border-radius: 1rem;
  background: #fafbff;
}

.empty-icon {
  font-size: 2rem;
  color: #8a94a6;
  margin-bottom: 0.5rem;
}

.filter-stack {
  display: flex;
  flex-direction: column;
  gap: 0.6rem;
}

.filter-chip {
  border: 1px solid #e5e7eb;
  background: #fff;
  color: #4b5563;
  padding: 0.8rem 0.9rem;
  border-radius: 14px;
  text-align: left;
  font-weight: 600;
  display: flex;
  align-items: center;
  justify-content: space-between;
  transition: all 0.2s ease;
}

.filter-chip.active {
  border-color: #bcd5ff;
  background: #eef4ff;
  color: #0d6efd;
}

.chip-count {
  min-width: 1.9rem;
  text-align: center;
  padding: 0.15rem 0.45rem;
  border-radius: 999px;
  background: #f1f5f9;
  color: #6b7280;
  font-size: 0.78rem;
}

.filter-chip.active .chip-count {
  background: #fff;
  color: #0d6efd;
}

.deadline-item {
  padding: 0.9rem;
  border: 1px solid #e9ecef;
  border-radius: 14px;
  background: #fff;
}

.deadline-badge {
  display: inline-flex;
  align-items: center;
  padding: 0.35rem 0.55rem;
  border-radius: 999px;
  background: #eef4ff;
  color: #0d6efd;
  font-size: 0.78rem;
  font-weight: 700;
}

.sidebar-empty {
  min-height: 160px;
  display: grid;
  place-items: center;
  text-align: center;
  border: 1px dashed #d9dee7;
  border-radius: 1rem;
  padding: 1rem;
  background: #fafbff;
}

.sidebar-empty-icon {
  color: #8a94a6;
  font-size: 1.5rem;
  margin-bottom: 0.5rem;
}
</style>
