<template>
  <StudentLayout v-model:search-query="searchQuery">
    <PageHeader
      title="Placements"
      subtitle="View offers, joining dates, and download confirmations."
    >
      <template #actions>
        <div class="d-flex flex-wrap gap-2">
          <RouterLink
            to="/student/applications"
            class="btn btn-outline-primary"
          >
            <i class="ti ti-file-text me-2"></i>Applications
          </RouterLink>
          <RouterLink to="/student/profile" class="btn btn-primary">
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
        >Complete your profile to keep placement records and eligibility
        accurate.</span
      >
    </div>

    <div v-if="store.error" class="alert alert-danger">
      {{ store.error }}
    </div>

    <div class="placements-shell">
      <div class="placements-hero card shadow-sm border-0 mb-4">
        <div
          class="card-body p-4 p-lg-5 d-flex flex-column flex-lg-row gap-4 align-items-lg-center justify-content-between"
        >
          <div>
            <span class="hero-kicker">Placements</span>
            <h3 class="fw-bold mb-2">Track offers and final outcomes</h3>
            <p class="text-muted mb-0">
              Review placement records, joining dates, salary details, and offer
              letter availability.
            </p>
          </div>

          <div class="d-flex flex-wrap gap-2">
            <RouterLink to="/student/drives" class="btn btn-outline-primary">
              <i class="ti ti-briefcase me-2"></i>Browse Drives
            </RouterLink>
            <RouterLink to="/student/applications" class="btn btn-primary">
              <i class="ti ti-send me-2"></i>Applications
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
                  <h6 class="fw-semibold mb-1">Placement records</h6>
                  <small class="text-muted">
                    {{ filteredPlacements.length }} placement{{
                      filteredPlacements.length === 1 ? "" : "s"
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
                    <option value="salary">Sort by salary</option>
                  </select>
                </div>
              </div>

              <div class="placement-list">
                <div
                  v-for="item in filteredPlacements"
                  :key="item.placementKey"
                  class="placement-card"
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
                          <span class="status-badge status-selected"
                            >Placed</span
                          >
                        </div>

                        <div
                          class="text-muted small d-flex flex-wrap align-items-center gap-2"
                        >
                          <span>{{ item.company }}</span>
                          <span v-if="item.salary"
                            >• {{ item.salaryLabel }}</span
                          >
                          <span v-if="item.joining_date"
                            >• Joining {{ item.joiningLabel }}</span
                          >
                        </div>

                        <div class="d-flex flex-wrap gap-2 mt-3">
                          <span
                            v-if="item.offer_letter_available"
                            class="badge rounded-pill text-bg-light border text-success"
                          >
                            Offer letter available
                          </span>
                          <span
                            v-else
                            class="badge rounded-pill text-bg-light border text-secondary"
                          >
                            Offer letter pending
                          </span>
                        </div>
                      </div>
                    </div>

                    <div class="text-lg-end">
                      <div class="small text-muted mb-1">Placed on</div>
                      <div class="fw-semibold">{{ item.createdLabel }}</div>
                      <div class="small text-muted mt-1">
                        {{
                          item.joining_date
                            ? "Joining scheduled"
                            : "Joining date pending"
                        }}
                      </div>
                    </div>
                  </div>

                  <div
                    class="placement-footer mt-3 pt-3 border-top d-flex flex-wrap justify-content-between align-items-center gap-2"
                  >
                    <div class="small text-muted">
                      {{
                        item.offer_letter_available
                          ? "Download the offer letter from here."
                          : "The company has not uploaded an offer letter yet."
                      }}
                    </div>

                    <div class="d-flex flex-wrap gap-2">
                      <RouterLink
                        :to="`/student/drives/${item.drive_id}`"
                        class="btn btn-outline-primary btn-sm"
                      >
                        View Drive
                      </RouterLink>

                      <button
                        v-if="item.offer_letter_available"
                        type="button"
                        class="btn btn-primary btn-sm"
                        @click="downloadOfferLetter(item)"
                      >
                        Download Offer Letter
                      </button>
                    </div>
                  </div>
                </div>
              </div>

              <div v-if="!filteredPlacements.length" class="empty-wrap mt-4">
                <div class="empty-state">
                  <i class="ti ti-trophy-off empty-icon"></i>
                  <div class="fw-semibold mb-1">No placements found</div>
                  <small class="text-muted d-block mb-3">
                    Placement records will appear here once a company selects
                    you.
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
                    >Jump between placement states</small
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
                  <h6 class="fw-semibold mb-1">Placement summary</h6>
                  <small class="text-muted">Highlights from your offers</small>
                </div>
                <i class="ti ti-chart-dots text-primary"></i>
              </div>

              <div v-if="placements.length" class="summary-stack">
                <div class="summary-item">
                  <div class="summary-label">Highest salary</div>
                  <div class="summary-value">{{ highestSalaryLabel }}</div>
                </div>
                <div class="summary-item">
                  <div class="summary-label">Next joining</div>
                  <div class="summary-value">{{ nextJoiningLabel }}</div>
                </div>
                <div class="summary-item">
                  <div class="summary-label">Offer letters</div>
                  <div class="summary-value">{{ offerLetterCount }}</div>
                </div>
              </div>

              <div v-else class="sidebar-empty">
                <i class="ti ti-trophy-off sidebar-empty-icon"></i>
                <div class="fw-semibold">No placement data yet</div>
                <small class="text-muted"
                  >Final results will show up here.</small
                >
              </div>
            </div>
          </div>

          <div class="card shadow-sm border-0">
            <div class="card-body p-4">
              <h6 class="fw-semibold mb-2">Need to prepare?</h6>
              <p class="text-muted small mb-3">
                Keep your profile and resume updated so you stay ready for final
                offers.
              </p>
              <div class="d-flex flex-wrap gap-2">
                <RouterLink
                  to="/student/profile"
                  class="btn btn-outline-primary btn-sm"
                >
                  Update Profile
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
import { useStudentStore } from "@/stores/studentStore";

const store = useStudentStore();
const { placements } = storeToRefs(store);

const searchQuery = ref("");
const activeTab = ref("all");
const sortBy = ref("latest");

const normalize = (value = "") => String(value).toLowerCase().trim();

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

const formatSalary = (value) => {
  if (value === null || value === undefined || value === "") return "";
  const num = Number(value);
  if (Number.isNaN(num)) return String(value);
  return `₹${num.toLocaleString("en-IN")}`;
};

const safePlacements = computed(() =>
  (placements.value || []).map((item) => ({
    ...item,
    placementKey:
      item.placement_id ||
      `${item.company}-${item.job_title}-${item.created_at || ""}`,
    companyInitials:
      String(item.company || "CO")
        .split(" ")
        .filter(Boolean)
        .slice(0, 2)
        .map((part) => part[0]?.toUpperCase())
        .join("") || "CO",
    salaryLabel: item.salary ? formatSalary(item.salary) : "Salary not shared",
    joiningLabel: item.joining_date ? formatDate(item.joining_date) : "TBA",
    createdLabel: item.created_at ? formatDate(item.created_at) : "Recent",
  })),
);

const statsCards = computed(() => [
  {
    label: "Placements",
    value: safePlacements.value.length,
    delta: "Final offers received",
    icon: "ti-trophy",
  },
  {
    label: "Offer Letters",
    value: safePlacements.value.filter((p) => p.offer_letter_available).length,
    delta: "Available to download",
    icon: "ti-file-download",
  },
  {
    label: "Joining Soon",
    value: safePlacements.value.filter((p) => p.joining_date).length,
    delta: "Scheduled joinings",
    icon: "ti-calendar-event",
  },
  {
    label: "Latest Update",
    value: safePlacements.value.length ? "Live" : "—",
    delta: "Placement records",
    icon: "ti-activity",
  },
]);

const tabs = computed(() => [
  { key: "all", label: "All", count: safePlacements.value.length },
  {
    key: "letter",
    label: "Offer Letter",
    count: safePlacements.value.filter((p) => p.offer_letter_available).length,
  },
  {
    key: "joining",
    label: "Joining Soon",
    count: safePlacements.value.filter((p) => p.joining_date).length,
  },
]);

const filterChips = tabs;

const filteredPlacements = computed(() => {
  let items = [...safePlacements.value];

  if (activeTab.value === "letter") {
    items = items.filter((item) => item.offer_letter_available);
  } else if (activeTab.value === "joining") {
    items = items.filter((item) => item.joining_date);
  }

  const query = normalize(searchQuery.value);
  if (query) {
    items = items.filter((item) => {
      const fields = [
        item.company,
        item.job_title,
        item.salaryLabel,
        item.joiningLabel,
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
    if (sortBy.value === "salary") {
      const aSalary = Number(a.salary || 0);
      const bSalary = Number(b.salary || 0);
      return bSalary - aSalary;
    }
    return (
      new Date(b.created_at || 0).getTime() -
      new Date(a.created_at || 0).getTime()
    );
  });

  return items;
});

const highestSalaryLabel = computed(() => {
  const top = [...safePlacements.value]
    .filter(
      (p) => p.salary !== undefined && p.salary !== null && p.salary !== "",
    )
    .sort((a, b) => Number(b.salary) - Number(a.salary))[0];

  return top ? `${formatSalary(top.salary)} · ${top.company}` : "Not shared";
});

const nextJoiningLabel = computed(() => {
  const upcoming = [...safePlacements.value]
    .filter((p) => p.joining_date)
    .sort((a, b) => new Date(a.joining_date) - new Date(b.joining_date))[0];

  return upcoming
    ? `${formatDate(upcoming.joining_date)} · ${upcoming.company}`
    : "No joining date";
});

const offerLetterCount = computed(
  () => safePlacements.value.filter((p) => p.offer_letter_available).length,
);

const statusLabel = () => "Placed";

const resetFilters = () => {
  activeTab.value = "all";
  sortBy.value = "latest";
  searchQuery.value = "";
};

const downloadOfferLetter = (item) => {
  const a = document.createElement("a");
  a.href = `/api/student/placements/${item.placement_id}/offer-letter`;
  a.target = "_blank";
  a.rel = "noreferrer";
  a.click();
};

onMounted(async () => {
  await Promise.allSettled([store.fetchProfile?.(), store.fetchPlacements?.()]);
});
</script>

<style scoped>
.placements-shell {
  display: flex;
  flex-direction: column;
  gap: 1.25rem;
}

.placements-hero {
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

.placement-list {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.placement-card {
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

.status-selected {
  background: #e8f8ef;
  color: #047857;
}

.placement-footer {
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
