<template>
  <StudentLayout v-model:search-query="searchQuery">
    <PageHeader
      title="Jobs & Drives"
      subtitle="Search and apply to approved placement drives."
    >
      <template #actions>
        <div class="d-flex flex-wrap gap-2">
          <RouterLink
            to="/student/applications"
            class="btn btn-outline-primary"
          >
            <i class="ti ti-file-text me-2"></i>Applications
          </RouterLink>
          <RouterLink to="/student/profile" class="btn btn-outline-primary">
            <i class="ti ti-user-edit me-2"></i>Profile
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
        >Complete your profile to unlock eligibility-based drive
        recommendations.</span
      >
    </div>

    <div v-if="store.error" class="alert alert-danger">
      {{ store.error }}
    </div>

    <div class="drive-shell">
      <div class="drive-hero card shadow-sm border-0 mb-4">
        <div
          class="card-body p-4 p-lg-5 d-flex flex-column flex-lg-row gap-4 align-items-lg-center justify-content-between"
        >
          <div>
            <span class="hero-kicker">Placement Drives</span>
            <h3 class="fw-bold mb-2">Find roles that match your profile</h3>
            <p class="text-muted mb-0">
              Browse eligible drives, track your application state, and jump
              into interviews faster.
            </p>
          </div>

          <div class="hero-actions d-flex flex-wrap gap-2">
            <RouterLink
              to="/student/placements"
              class="btn btn-outline-primary"
            >
              <i class="ti ti-trophy me-2"></i>Placements
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
        </button>
      </div>

      <div class="row g-4 align-items-start">
        <div class="col-12 col-xl-8">
          <div class="card shadow-sm border-0 mb-4">
            <div class="card-body p-4">
              <div
                class="d-flex flex-column flex-lg-row gap-3 justify-content-between align-items-lg-center mb-4"
              >
                <div>
                  <h6 class="fw-semibold mb-1">Drive listings</h6>
                  <small class="text-muted">
                    {{ filteredDrives.length }} drive{{
                      filteredDrives.length === 1 ? "" : "s"
                    }}
                    shown
                  </small>
                </div>

                <div class="d-flex flex-wrap gap-2 align-items-center">
                  <select
                    v-model="sortBy"
                    class="form-select form-select-sm sort-select"
                  >
                    <option value="deadline">Sort by deadline</option>
                    <option value="company">Sort by company</option>
                    <option value="title">Sort by role</option>
                    <option value="salary">Sort by salary</option>
                  </select>
                </div>
              </div>

              <div class="drive-grid">
                <StudentDriveCard
                  v-for="drive in filteredDrives"
                  :key="drive.cardKey"
                  :drive="drive"
                  :action-label="
                    applyingDriveId === drive.drive_id
                      ? 'Applying...'
                      : driveActionLabel(drive)
                  "
                  :disabled="
                    drive.actionDisabled ||
                    applyingDriveId === drive.drive_id
                  "
                  @action="handleApply(drive)"
                />
              </div>

              <div v-if="!filteredDrives.length" class="empty-wrap mt-4">
                <div class="empty-state">
                  <i class="ti ti-briefcase-off empty-icon"></i>
                  <div class="fw-semibold mb-1">
                    No drives match your filters
                  </div>
                  <small class="text-muted d-block mb-3">
                    Try a different search term or switch back to All drives.
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
                      to="/student/profile"
                      class="btn btn-primary btn-sm"
                    >
                      Update Profile
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
                  <small class="text-muted">Narrow down the drive list</small>
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
                  <h6 class="fw-semibold mb-1">Upcoming deadlines</h6>
                  <small class="text-muted">Next drives closing soon</small>
                </div>
                <RouterLink
                  to="/student/applications"
                  class="link-primary small text-decoration-none"
                >
                  View applications
                </RouterLink>
              </div>

              <div v-if="upcomingDeadlines.length" class="deadline-list">
                <div
                  v-for="drive in upcomingDeadlines"
                  :key="`deadline-${drive.cardKey}`"
                  class="deadline-item"
                >
                  <div class="d-flex justify-content-between gap-3">
                    <div>
                      <div class="fw-semibold">
                        {{ drive.job_title || "Drive" }}
                      </div>
                      <small class="text-muted">{{
                        drive.company_name || drive.company?.name || "Company"
                      }}</small>
                    </div>
                    <span class="deadline-badge">{{
                      deadlineLabel(drive)
                    }}</span>
                  </div>
                </div>
              </div>

              <div v-else class="sidebar-empty">
                <i class="ti ti-calendar-off sidebar-empty-icon"></i>
                <div class="fw-semibold">No closing drives</div>
                <small class="text-muted"
                  >New drives will appear here when available.</small
                >
              </div>
            </div>
          </div>

          <div class="card shadow-sm border-0">
            <div class="card-body p-4">
              <h6 class="fw-semibold mb-2">Need the next step?</h6>
              <p class="text-muted small mb-3">
                Keep your profile updated so eligibility-based drives stay
                accurate.
              </p>
              <div class="d-flex flex-wrap gap-2">
                <RouterLink
                  to="/student/profile"
                  class="btn btn-outline-primary btn-sm"
                >
                  Complete Profile
                </RouterLink>
                <RouterLink
                  to="/student/interviews"
                  class="btn btn-outline-secondary btn-sm"
                >
                  Interviews
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
import StudentDriveCard from "@/components/student/StudentDriveCard.vue";
import { useStudentStore } from "@/stores/studentStore";

const store = useStudentStore();
const { dashboard, profile } = storeToRefs(store);

const searchQuery = ref("");
const activeTab = ref("all");
const sortBy = ref("deadline");
const applyingDriveId = ref(null);

const tabs = [
  { key: "all", label: "All" },
  { key: "eligible", label: "Eligible" },
  { key: "applied", label: "Applied" },
  { key: "shortlisted", label: "Shortlisted" },
  { key: "selected", label: "Selected" },
];

const normalize = (value = "") => String(value).toLowerCase().trim();

const flattenDrive = (source, status, extra = {}) => {
  const drive = source?.drive || source || {};
  return {
    ...drive,
    ...extra,
    cardKey:
      drive.drive_id ||
      extra.application_id ||
      `${status}-${drive.job_title || "drive"}`,
    driveStatus: status,
    application_id: extra.application_id || null,
    application_date: extra.application_date || null,
    interview_date: extra.interview_date || null,
    interview_type: extra.interview_type || null,
    remarks: extra.remarks || null,
    actionDisabled: status !== "eligible",
  };
};

const mergedDrives = computed(() => {
  const items = [];
  const seen = new Map();

  const upsert = (item) => {
    const id = item.drive_id;
    if (!id) return;

    const priority = {
      selected: 4,
      shortlisted: 3,
      applied: 2,
      eligible: 1,
    };

    const existing = seen.get(id);
    if (
      !existing ||
      priority[item.driveStatus] > priority[existing.driveStatus]
    ) {
      seen.set(id, item);
    }
  };

  for (const drive of dashboard.value?.eligible_drives || []) {
    upsert(flattenDrive(drive, "eligible"));
  }

  for (const app of dashboard.value?.applied_drives || []) {
    upsert(flattenDrive(app.drive, "applied", app));
  }

  for (const app of dashboard.value?.shortlisted_drives || []) {
    upsert(flattenDrive(app.drive, "shortlisted", app));
  }

  for (const app of dashboard.value?.selected_drives || []) {
    upsert(flattenDrive(app.drive, "selected", app));
  }

  items.push(...seen.values());

  return items;
});

const activeCount = computed(
  () =>
    mergedDrives.value.filter((drive) => drive.driveStatus === "eligible")
      .length,
);

const appliedCount = computed(() => dashboard.value?.counts?.applied || 0);
const shortlistedCount = computed(
  () => dashboard.value?.counts?.shortlisted || 0,
);
const selectedCount = computed(() => dashboard.value?.counts?.selected || 0);
const eligibleCount = computed(() => dashboard.value?.counts?.eligible || 0);

const statsCards = computed(() => [
  {
    label: "Eligible Drives",
    value: eligibleCount.value,
    delta: "Recommended for you",
    icon: "ti-briefcase",
  },
  {
    label: "Applications",
    value: appliedCount.value,
    delta: "Submitted so far",
    icon: "ti-send",
  },
  {
    label: "Shortlisted",
    value: shortlistedCount.value,
    delta: "Interview stage",
    icon: "ti-star",
  },
  {
    label: "Selected",
    value: selectedCount.value,
    delta: "Offers received",
    icon: "ti-trophy",
  },
]);

const filterChips = computed(() => [
  { key: "all", label: "All drives", count: mergedDrives.value.length },
  {
    key: "eligible",
    label: "Eligible",
    count: mergedDrives.value.filter((d) => d.driveStatus === "eligible")
      .length,
  },
  {
    key: "applied",
    label: "Applied",
    count: mergedDrives.value.filter((d) => d.driveStatus === "applied").length,
  },
  {
    key: "shortlisted",
    label: "Shortlisted",
    count: mergedDrives.value.filter((d) => d.driveStatus === "shortlisted")
      .length,
  },
  {
    key: "selected",
    label: "Selected",
    count: mergedDrives.value.filter((d) => d.driveStatus === "selected")
      .length,
  },
]);

const filteredDrives = computed(() => {
  let items = [...mergedDrives.value];

  const tab = activeTab.value;
  if (tab !== "all") {
    items = items.filter((drive) => drive.driveStatus === tab);
  }

  const query = normalize(searchQuery.value);
  if (query) {
    items = items.filter((drive) => {
      const companyName = drive.company_name || drive.company?.name || "";
      const title = drive.job_title || "";
      const skills = drive.required_skills || drive.skills_required || "";
      const location = drive.job_location || "";
      const type = drive.job_type || "";
      return [companyName, title, skills, location, type].some((field) =>
        normalize(field).includes(query),
      );
    });
  }

  items.sort((a, b) => {
    if (sortBy.value === "company") {
      return normalize(a.company_name || a.company?.name || "").localeCompare(
        normalize(b.company_name || b.company?.name || ""),
      );
    }

    if (sortBy.value === "title") {
      return normalize(a.job_title || "").localeCompare(
        normalize(b.job_title || ""),
      );
    }

    if (sortBy.value === "salary") {
      const aSalary = Number(a.salary ?? a.salary_min ?? a.min_salary ?? 0);
      const bSalary = Number(b.salary ?? b.salary_min ?? b.min_salary ?? 0);
      return bSalary - aSalary;
    }

    const aDate = new Date(a.application_deadline || a.deadline || 0).getTime();
    const bDate = new Date(b.application_deadline || b.deadline || 0).getTime();
    return aDate - bDate;
  });

  return items;
});

const upcomingDeadlines = computed(() =>
  filteredDrives.value
    .filter((drive) => drive.application_deadline || drive.deadline)
    .slice(0, 4),
);

const driveActionLabel = (drive) => {
  if (drive.driveStatus === "eligible") return "Apply Now";
  if (drive.driveStatus === "applied") return "Applied";
  if (drive.driveStatus === "shortlisted") return "Shortlisted";
  if (drive.driveStatus === "selected") return "Selected";
  return "View Details";
};

const handleApply = async (drive) => {
  if (!drive?.drive_id || drive.driveStatus !== "eligible") return;

  if (
    !window.confirm(
      `Apply to ${drive.job_title || "this drive"} at ${
        drive.company_name || drive.company?.name || "this company"
      }?`,
    )
  ) {
    return;
  }

  applyingDriveId.value = drive.drive_id;
  try {
    await store.applyToDrive(drive.drive_id);
  } finally {
    applyingDriveId.value = null;
  }
};

const deadlineLabel = (drive) => {
  const value = drive.application_deadline || drive.deadline;
  if (!value) return "No deadline";
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
  sortBy.value = "deadline";
  searchQuery.value = "";
};

onMounted(async () => {
  await Promise.allSettled([store.fetchProfile?.(), store.fetchDashboard?.()]);
});
</script>

<style scoped>
.drive-shell {
  display: flex;
  flex-direction: column;
  gap: 1.25rem;
}

.drive-hero {
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
}

.tab-pill.active {
  background: #fff;
  color: #0d6efd;
  box-shadow: 0 8px 20px rgba(15, 23, 42, 0.06);
}

.sort-select {
  min-width: 180px;
}

.drive-grid {
  display: grid;
  gap: 1rem;
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
