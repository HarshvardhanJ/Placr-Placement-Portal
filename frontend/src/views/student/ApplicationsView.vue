<template>
  <StudentLayout v-model:search-query="searchQuery">
    <PageHeader
      title="Applications"
      subtitle="Track submitted applications and shortlist status."
    >
      <template #actions>
        <div class="d-flex flex-wrap gap-2">
          <RouterLink to="/student/drives" class="btn btn-primary">
            <i class="ti ti-briefcase me-2"></i>Browse Drives
          </RouterLink>
          <RouterLink to="/student/interviews" class="btn btn-outline-primary">
            <i class="ti ti-calendar-event me-2"></i>Interviews
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
        >Complete your profile to improve application matching and shortlist
        visibility.</span
      >
    </div>

    <div v-if="store.error" class="alert alert-danger">
      {{ store.error }}
    </div>

    <div class="applications-shell">
      <div class="applications-hero card shadow-sm border-0 mb-4">
        <div
          class="card-body p-4 p-lg-5 d-flex flex-column flex-lg-row gap-4 align-items-lg-center justify-content-between"
        >
          <div>
            <span class="hero-kicker">Applications</span>
            <h3 class="fw-bold mb-2">Monitor every submission in one place</h3>
            <p class="text-muted mb-0">
              View application state, shortlist progress, interview updates, and
              placement outcomes.
            </p>
          </div>

          <div class="d-flex flex-wrap gap-2">
            <RouterLink to="/student/profile" class="btn btn-outline-primary">
              <i class="ti ti-user-edit me-2"></i>Update Profile
            </RouterLink>
            <RouterLink to="/student/placements" class="btn btn-primary">
              <i class="ti ti-trophy me-2"></i>Placements
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
                  <h6 class="fw-semibold mb-1">Your applications</h6>
                  <small class="text-muted">
                    {{ filteredApplications.length }} application{{
                      filteredApplications.length === 1 ? "" : "s"
                    }}
                    shown
                  </small>
                </div>

                <div class="d-flex flex-wrap gap-2">
                  <select
                    v-model="sortBy"
                    class="form-select form-select-sm sort-select"
                  >
                    <option value="latest">Sort by latest</option>
                    <option value="company">Sort by company</option>
                    <option value="role">Sort by role</option>
                    <option value="status">Sort by status</option>
                  </select>
                </div>
              </div>

              <div class="application-list">
                <div
                  v-for="app in filteredApplications"
                  :key="app.applicationKey"
                  class="application-card"
                >
                  <div
                    class="d-flex flex-column flex-lg-row gap-3 justify-content-between"
                  >
                    <div class="d-flex gap-3">
                      <div class="company-logo">
                        {{ app.companyInitials }}
                      </div>

                      <div>
                        <div
                          class="d-flex flex-wrap align-items-center gap-2 mb-1"
                        >
                          <h5 class="mb-0 fw-semibold">{{ app.job_title }}</h5>
                          <span
                            class="status-badge"
                            :class="statusClass(app.status)"
                          >
                            {{ statusLabel(app.status) }}
                          </span>
                        </div>

                        <div
                          class="text-muted small d-flex flex-wrap align-items-center gap-2"
                        >
                          <span>{{ app.company_name }}</span>
                          <span v-if="app.job_location"
                            >• {{ app.job_location }}</span
                          >
                          <span v-if="app.job_type">• {{ app.job_type }}</span>
                        </div>

                        <div class="d-flex flex-wrap gap-2 mt-3">
                          <span
                            v-for="skill in app.skillTags"
                            :key="skill"
                            class="badge rounded-pill text-bg-light border text-secondary"
                          >
                            {{ skill }}
                          </span>
                        </div>
                      </div>
                    </div>

                    <div class="text-lg-end">
                      <div class="small text-muted mb-1">Applied</div>
                      <div class="fw-semibold">{{ app.appliedLabel }}</div>
                      <div
                        v-if="app.interview_date"
                        class="small text-muted mt-1"
                      >
                        Interview: {{ app.interviewLabel }}
                      </div>
                    </div>
                  </div>

                  <div
                    class="application-footer mt-3 pt-3 border-top d-flex flex-wrap justify-content-between align-items-center gap-2"
                  >
                    <div class="small text-muted">
                      {{ app.feedbackLabel }}
                    </div>

                    <div class="d-flex flex-wrap gap-2">
                      <RouterLink
                        :to="`/student/drives/${app.drive_id}`"
                        class="btn btn-outline-primary btn-sm"
                      >
                        View Drive
                      </RouterLink>
                      <RouterLink
                        v-if="app.interview_date"
                        to="/student/interviews"
                        class="btn btn-primary btn-sm"
                      >
                        Interview Details
                      </RouterLink>
                    </div>
                  </div>
                </div>
              </div>

              <div v-if="!filteredApplications.length" class="empty-wrap mt-4">
                <div class="empty-state">
                  <i class="ti ti-file-off empty-icon"></i>
                  <div class="fw-semibold mb-1">No applications found</div>
                  <small class="text-muted d-block mb-3">
                    Try a different search or switch to another application
                    status.
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
                    >Jump between application states</small
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
                  <h6 class="fw-semibold mb-1">Upcoming interviews</h6>
                  <small class="text-muted">Next scheduled rounds</small>
                </div>
                <RouterLink
                  to="/student/interviews"
                  class="link-primary small text-decoration-none"
                >
                  View all
                </RouterLink>
              </div>

              <div v-if="upcomingInterviews.length" class="deadline-list">
                <div
                  v-for="item in upcomingInterviews"
                  :key="item.applicationKey"
                  class="deadline-item"
                >
                  <div class="d-flex justify-content-between gap-3">
                    <div>
                      <div class="fw-semibold">{{ item.job_title }}</div>
                      <small class="text-muted">{{ item.company_name }}</small>
                    </div>
                    <span class="deadline-badge">{{
                      item.interviewLabel
                    }}</span>
                  </div>
                </div>
              </div>

              <div v-else class="sidebar-empty">
                <i class="ti ti-calendar-off sidebar-empty-icon"></i>
                <div class="fw-semibold">No interviews yet</div>
                <small class="text-muted"
                  >Shortlisted drives will appear here.</small
                >
              </div>
            </div>
          </div>

          <div class="card shadow-sm border-0">
            <div class="card-body p-4">
              <h6 class="fw-semibold mb-2">Need to improve your odds?</h6>
              <p class="text-muted small mb-3">
                Keep your CGPA, skills, and resume updated so companies can
                shortlist you faster.
              </p>
              <div class="d-flex flex-wrap gap-2">
                <RouterLink
                  to="/student/profile"
                  class="btn btn-outline-primary btn-sm"
                >
                  Complete Profile
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
const sortBy = ref("latest");

const tabs = [
  { key: "all", label: "All" },
  { key: "applied", label: "Applied" },
  { key: "shortlisted", label: "Shortlisted" },
  { key: "selected", label: "Selected" },
];

const normalize = (value = "") => String(value).toLowerCase().trim();

const flattenApplication = (source, status) => {
  const drive = source?.drive || source || {};
  return {
    applicationKey:
      source.application_id ||
      drive.drive_id ||
      `${status}-${drive.job_title || "app"}`,
    application_id: source.application_id || null,
    drive_id: drive.drive_id,
    status,
    job_title: drive.job_title || "Drive",
    company_name: drive.company_name || drive.company?.name || "Company",
    job_location: drive.job_location || "",
    job_type: drive.job_type || "",
    skills_raw: drive.required_skills || drive.skills_required || "",
    applied_on:
      source.application_date || source.applied_on || source.created_at || null,
    interview_date: source.interview_date || null,
    interview_type: source.interview_type || "",
    feedback: source.feedback || source.remarks || "",
    drive,
  };
};

const applications = computed(() => {
  const list = [];

  for (const item of dashboard.value?.applied_drives || []) {
    list.push(flattenApplication(item, "applied"));
  }

  for (const item of dashboard.value?.shortlisted_drives || []) {
    list.push(flattenApplication(item, "shortlisted"));
  }

  for (const item of dashboard.value?.selected_drives || []) {
    list.push(flattenApplication(item, "selected"));
  }

  const byDrive = new Map();
  for (const app of list) {
    const existing = byDrive.get(app.drive_id);
    const priority = { selected: 3, shortlisted: 2, applied: 1 };
    if (!existing || priority[app.status] > priority[existing.status]) {
      byDrive.set(app.drive_id, app);
    }
  }

  return [...byDrive.values()];
});

const counts = computed(() => dashboard.value?.counts || {});

const statsCards = computed(() => [
  {
    label: "Applications",
    value: Number(counts.value.applied || 0),
    delta: "Submitted so far",
    icon: "ti-send",
  },
  {
    label: "Shortlisted",
    value: Number(counts.value.shortlisted || 0),
    delta: "Interview stage",
    icon: "ti-star",
  },
  {
    label: "Selected",
    value: Number(counts.value.selected || 0),
    delta: "Offers received",
    icon: "ti-trophy",
  },
  {
    label: "Eligible",
    value: Number(counts.value.eligible || 0),
    delta: "Recommended drives",
    icon: "ti-briefcase",
  },
]);

const filterChips = computed(() => [
  { key: "all", label: "All applications", count: applications.value.length },
  {
    key: "applied",
    label: "Applied",
    count: applications.value.filter((a) => a.status === "applied").length,
  },
  {
    key: "shortlisted",
    label: "Shortlisted",
    count: applications.value.filter((a) => a.status === "shortlisted").length,
  },
  {
    key: "selected",
    label: "Selected",
    count: applications.value.filter((a) => a.status === "selected").length,
  },
]);

const skillTags = (raw) =>
  String(raw || "")
    .split(",")
    .map((item) => item.trim())
    .filter(Boolean)
    .slice(0, 4);

const filteredApplications = computed(() => {
  let items = [...applications.value];

  if (activeTab.value !== "all") {
    items = items.filter((item) => item.status === activeTab.value);
  }

  const query = normalize(searchQuery.value);
  if (query) {
    items = items.filter((item) => {
      const fields = [
        item.job_title,
        item.company_name,
        item.job_location,
        item.job_type,
        item.skills_raw,
      ];
      return fields.some((field) => normalize(field).includes(query));
    });
  }

  items.sort((a, b) => {
    if (sortBy.value === "company") {
      return normalize(a.company_name).localeCompare(normalize(b.company_name));
    }
    if (sortBy.value === "role") {
      return normalize(a.job_title).localeCompare(normalize(b.job_title));
    }
    if (sortBy.value === "status") {
      return normalize(statusLabel(a.status)).localeCompare(
        normalize(statusLabel(b.status)),
      );
    }
    return (
      new Date(b.applied_on || 0).getTime() -
      new Date(a.applied_on || 0).getTime()
    );
  });

  return items.map((item) => ({
    ...item,
    companyInitials:
      item.company_name
        .split(" ")
        .filter(Boolean)
        .slice(0, 2)
        .map((part) => part[0]?.toUpperCase())
        .join("") || "CO",
    skillTags: skillTags(item.skills_raw),
    appliedLabel: formatDate(item.applied_on) || "Recent",
    interviewLabel: formatDate(item.interview_date) || "TBA",
    feedbackLabel: item.feedback || "No feedback shared yet.",
  }));
});

const upcomingInterviews = computed(() =>
  filteredApplications.value.filter((item) => item.interview_date).slice(0, 4),
);

const statusLabel = (status) => {
  if (status === "applied") return "Applied";
  if (status === "shortlisted") return "Shortlisted";
  if (status === "selected") return "Selected";
  if (status === "rejected") return "Rejected";
  return "Unknown";
};

const statusClass = (status) => {
  if (status === "applied") return "status-applied";
  if (status === "shortlisted") return "status-shortlisted";
  if (status === "selected") return "status-selected";
  if (status === "rejected") return "status-rejected";
  return "status-muted";
};

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

const resetFilters = () => {
  activeTab.value = "all";
  sortBy.value = "latest";
  searchQuery.value = "";
};

onMounted(async () => {
  await Promise.allSettled([store.fetchProfile?.(), store.fetchDashboard?.()]);
});
</script>

<style scoped>
.applications-shell {
  display: flex;
  flex-direction: column;
  gap: 1.25rem;
}

.applications-hero {
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

.application-list {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.application-card {
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

.status-applied {
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

.status-rejected {
  background: #fee2e2;
  color: #b91c1c;
}

.status-muted {
  background: #f1f5f9;
  color: #64748b;
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

.deadline-list {
  display: flex;
  flex-direction: column;
  gap: 0.8rem;
}

.deadline-item {
  padding: 0.9rem;
  border: 1px solid #e9ecef;
  border-radius: 14px;
  background: #fff;
}

.deadline-badge {
  white-space: nowrap;
  align-self: flex-start;
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
