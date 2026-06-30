<template>
  <StudentLayout v-model:search-query="searchQuery">
    <PageHeader
      :title="drive?.job_title || 'Drive Details'"
      :subtitle="drive?.company_name || 'Approved placement drive'"
    >
      <template #actions>
        <div class="d-flex flex-wrap gap-2">
          <RouterLink to="/student/drives" class="btn btn-outline-primary">
            <i class="ti ti-arrow-left me-2"></i>Back
          </RouterLink>
          <button
            v-if="canApply"
            type="button"
            class="btn btn-primary"
            :disabled="applying"
            @click="handleApply"
          >
            <span
              v-if="applying"
              class="spinner-border spinner-border-sm me-2"
            ></span>
            Apply Now
          </button>
        </div>
      </template>
    </PageHeader>

    <div v-if="error" class="alert alert-danger">
      {{ error }}
    </div>

    <div v-if="loading" class="card shadow-sm border-0 p-5 text-center">
      Loading drive details...
    </div>

    <template v-else-if="drive">
      <div class="drive-detail-shell">
        <div class="drive-hero card shadow-sm border-0 mb-4">
          <div class="card-body p-4 p-lg-5">
            <div
              class="d-flex flex-column flex-lg-row gap-4 justify-content-between"
            >
              <div class="flex-grow-1">
                <div class="d-flex flex-wrap align-items-center gap-2 mb-2">
                  <span class="hero-kicker">Placement Drive</span>
                  <span class="status-badge" :class="statusClass">
                    {{ statusLabel }}
                  </span>
                </div>

                <h3 class="fw-bold mb-2">{{ drive.job_title }}</h3>
                <p class="text-muted mb-3">
                  {{ drive.company_name || "Company" }} ·
                  {{ drive.job_location || "Location not specified" }}
                </p>

                <div class="d-flex flex-wrap gap-2">
                  <span class="meta-item">
                    <i class="ti ti-calendar-event me-1"></i>{{ deadlineLabel }}
                  </span>
                  <span class="meta-item">
                    <i class="ti ti-wallet me-1"></i>{{ salaryLabel }}
                  </span>
                  <span class="meta-item">
                    <i class="ti ti-user-check me-1"></i>{{ eligibilityLabel }}
                  </span>
                  <span class="meta-item">
                    <i class="ti ti-users me-1"></i
                    >{{ drive.applicants ?? 0 }} applicants
                  </span>
                </div>
              </div>

              <div class="company-card">
                <div class="company-avatar">{{ companyInitials }}</div>
                <div>
                  <div class="fw-semibold">
                    {{ drive.company_name || "Company" }}
                  </div>
                  <small class="text-muted">Approved placement drive</small>
                </div>
              </div>
            </div>
          </div>
        </div>

        <div class="row g-4 align-items-start">
          <div class="col-12 col-xl-8">
            <div class="card shadow-sm border-0 mb-4">
              <div class="card-body p-4">
                <h6 class="fw-semibold mb-3">Job description</h6>
                <p class="text-muted mb-0">
                  {{ drive.job_description || "No job description provided." }}
                </p>
              </div>
            </div>

            <div class="row g-4">
              <div class="col-12 col-md-6">
                <div class="card shadow-sm border-0 h-100">
                  <div class="card-body p-4">
                    <h6 class="fw-semibold mb-3">Requirements</h6>
                    <div class="detail-stack">
                      <div class="detail-item">
                        <div class="detail-label">Required skills</div>
                        <div class="detail-value">
                          {{ drive.required_skills || "Not specified" }}
                        </div>
                      </div>
                      <div class="detail-item">
                        <div class="detail-label">Experience</div>
                        <div class="detail-value">
                          {{
                            `${drive.experience_required} Year` ||
                            "Not specified"
                          }}
                        </div>
                      </div>
                      <div class="detail-item">
                        <div class="detail-label">Eligible branches</div>
                        <div class="detail-value">
                          {{ drive.eligible_branch || "All branches" }}
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
              </div>

              <div class="col-12 col-md-6">
                <div class="card shadow-sm border-0 h-100">
                  <div class="card-body p-4">
                    <h6 class="fw-semibold mb-3">Offer details</h6>
                    <div class="detail-stack">
                      <div class="detail-item">
                        <div class="detail-label">No. of openings</div>
                        <div class="detail-value">
                          {{ drive.no_openings ?? "—" }}
                        </div>
                      </div>
                      <div class="detail-item">
                        <div class="detail-label">Minimum CGPA</div>
                        <div class="detail-value">
                          {{ drive.min_cgpa ?? "Any" }}
                        </div>
                      </div>
                      <div class="detail-item">
                        <div class="detail-label">Eligible year</div>
                        <div class="detail-value">
                          {{ drive.year ?? "Any" }}
                        </div>
                      </div>
                      <div class="detail-item">
                        <div class="detail-label">Benefits</div>
                        <div class="detail-value">
                          {{ drive.benefits || "Not specified" }}
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>

            <div
              v-if="drive.required_skills"
              class="card shadow-sm border-0 mt-4"
            >
              <div class="card-body p-4">
                <h6 class="fw-semibold mb-3">Skill tags</h6>
                <div class="d-flex flex-wrap gap-2">
                  <span
                    v-for="skill in skillTags"
                    :key="skill"
                    class="badge rounded-pill text-bg-light border text-secondary"
                  >
                    {{ skill }}
                  </span>
                </div>
              </div>
            </div>
          </div>

          <div class="col-12 col-xl-4 d-flex flex-column gap-4">
            <div class="card shadow-sm border-0">
              <div class="card-body p-4">
                <h6 class="fw-semibold mb-3">Application status</h6>

                <div class="status-box">
                  <div
                    class="d-flex align-items-center justify-content-between mb-3"
                  >
                    <span class="small text-muted">Current status</span>
                    <span class="status-badge" :class="statusClass">
                      {{ statusLabel }}
                    </span>
                  </div>

                  <p class="text-muted small mb-3">
                    {{ statusHint }}
                  </p>

                  <div class="d-grid gap-2">
                    <button
                      v-if="canApply"
                      type="button"
                      class="btn btn-primary"
                      :disabled="applying"
                      @click="handleApply"
                    >
                      <span
                        v-if="applying"
                        class="spinner-border spinner-border-sm me-2"
                      ></span>
                      Apply Now
                    </button>
                    <RouterLink
                      v-else
                      to="/student/applications"
                      class="btn btn-outline-primary"
                    >
                      View Applications
                    </RouterLink>
                  </div>
                </div>
              </div>
            </div>

            <div class="card shadow-sm border-0">
              <div class="card-body p-4">
                <h6 class="fw-semibold mb-2">Need to prepare?</h6>
                <p class="text-muted small mb-3">
                  Keep your profile complete before applying so eligibility
                  checks pass smoothly.
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
    </template>

    <div v-else class="card shadow-sm border-0 p-5 text-center">
      <i class="ti ti-briefcase-off display-5 text-muted mb-3"></i>
      <h5 class="fw-semibold mb-2">Drive not found</h5>
      <p class="text-muted mb-0">
        This drive may have been removed or is not approved yet.
      </p>
    </div>
  </StudentLayout>
</template>

<script setup>
import { computed, onMounted, ref, watch } from "vue";
import { useRoute } from "vue-router";
import { storeToRefs } from "pinia";
import StudentLayout from "@/layouts/StudentLayout.vue";
import PageHeader from "@/components/shared/PageHeader.vue";
import { useStudentStore } from "@/stores/studentStore";
import studentApi from "@/services/studentApi";

const route = useRoute();
const store = useStudentStore();
const { dashboard, profile } = storeToRefs(store);

const searchQuery = ref("");
const loading = ref(false);
const applying = ref(false);
const drive = ref(null);
const error = ref(null);

const loadDrive = async () => {
  loading.value = true;
  error.value = null;

  try {
    drive.value = await studentApi.getDriveById(route.params.id);
  } catch (err) {
    error.value = err?.response?.data?.error || "Failed to load drive details";
    drive.value = null;
  } finally {
    loading.value = false;
  }
};

const profileComplete = computed(() =>
  Boolean(
    profile.value?.department && profile.value?.cgpa && profile.value?.year,
  ),
);

const appliedDriveIds = computed(() => {
  const ids = new Set();
  for (const item of dashboard.value?.applied_drives || []) {
    if (item.drive_id) ids.add(item.drive_id);
    if (item.drive?.drive_id) ids.add(item.drive.drive_id);
  }
  for (const item of dashboard.value?.shortlisted_drives || []) {
    if (item.drive_id) ids.add(item.drive_id);
    if (item.drive?.drive_id) ids.add(item.drive.drive_id);
  }
  for (const item of dashboard.value?.selected_drives || []) {
    if (item.drive_id) ids.add(item.drive_id);
    if (item.drive?.drive_id) ids.add(item.drive.drive_id);
  }
  return ids;
});

const isApplied = computed(() => appliedDriveIds.value.has(route.params.id));

const deadlineLabel = computed(() => {
  const value = drive.value?.application_deadline;
  if (!value) return "Deadline not set";
  const date = new Date(value);
  return Number.isNaN(date.getTime())
    ? String(value)
    : date.toLocaleDateString("en-GB", {
        day: "numeric",
        month: "short",
        year: "numeric",
      });
});

const salaryLabel = computed(() => {
  const salary = drive.value?.salary;
  if (salary === null || salary === undefined || salary === "")
    return "Salary not shared";
  const num = Number(salary);
  return Number.isNaN(num) ? String(salary) : `₹${num.toLocaleString("en-IN")}`;
});

const eligibilityLabel = computed(() => {
  if (drive.value?.year) return `Year ${drive.value.year}`;
  if (drive.value?.min_cgpa) return `Min CGPA ${drive.value.min_cgpa}`;
  return "Open eligibility";
});

const companyInitials = computed(() => {
  const value = drive.value?.company_name || "CO";
  return (
    value
      .split(" ")
      .filter(Boolean)
      .slice(0, 2)
      .map((part) => part[0]?.toUpperCase())
      .join("") || "CO"
  );
});

const skillTags = computed(() =>
  String(drive.value?.required_skills || "")
    .split(",")
    .map((item) => item.trim())
    .filter(Boolean)
    .slice(0, 8),
);

const canApply = computed(() => {
  if (!drive.value) return false;
  if (isApplied.value) return false;
  if (drive.value.approval_status !== "approved") return false;
  if (!profileComplete.value) return false;

  const deadline = drive.value.application_deadline
    ? new Date(drive.value.application_deadline)
    : null;
  if (deadline && !Number.isNaN(deadline.getTime()) && deadline < new Date()) {
    return false;
  }

  return true;
});

const statusClass = computed(() => {
  if (isApplied.value) return "status-applied";
  if (!profileComplete.value) return "status-muted";
  if (drive.value?.approval_status !== "approved") return "status-muted";
  return "status-open";
});

const statusLabel = computed(() => {
  if (isApplied.value) return "Applied";
  if (!profileComplete.value) return "Profile incomplete";
  if (drive.value?.approval_status !== "approved") return "Not open";
  return "Open";
});

const statusHint = computed(() => {
  if (isApplied.value) {
    return "You have already submitted an application for this drive.";
  }
  if (!profileComplete.value) {
    return "Complete your profile to unlock apply access.";
  }
  if (drive.value?.approval_status !== "approved") {
    return "This drive is not available for applications yet.";
  }
  return "Your profile matches this drive. You can apply now.";
});

const handleApply = async () => {
  if (!drive.value?.drive_id || !canApply.value) return;

  if (!window.confirm(`Apply to ${drive.value.job_title || "this drive"}?`)) {
    return;
  }

  applying.value = true;
  try {
    await store.applyToDrive(drive.value.drive_id);
    await Promise.allSettled([store.fetchDashboard(true), loadDrive()]);
  } catch (err) {
    error.value = err?.response?.data?.error || "Failed to submit application";
  } finally {
    applying.value = false;
  }
};

onMounted(async () => {
  await Promise.allSettled([
    store.fetchProfile(),
    store.fetchDashboard(),
    loadDrive(),
  ]);
});

watch(
  () => route.params.id,
  async () => {
    if (route.params.id) {
      await loadDrive();
    }
  },
);
</script>

<style scoped>
.drive-detail-shell {
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
}

.status-badge {
  display: inline-flex;
  align-items: center;
  padding: 0.3rem 0.6rem;
  border-radius: 999px;
  font-size: 0.78rem;
  font-weight: 700;
}

.status-open {
  background: #eef4ff;
  color: #0d6efd;
}

.status-applied {
  background: #e8f8ef;
  color: #047857;
}

.status-muted {
  background: #f1f5f9;
  color: #64748b;
}

.meta-item {
  display: inline-flex;
  align-items: center;
  gap: 0.15rem;
  padding: 0.45rem 0.7rem;
  border-radius: 999px;
  background: #f8fafc;
  border: 1px solid #e9ecef;
  color: #4b5563;
  font-size: 0.82rem;
}

.company-card {
  display: flex;
  align-items: center;
  gap: 0.8rem;
  padding: 0.95rem;
  border-radius: 16px;
  background: #fff;
  border: 1px solid #e9ecef;
  box-shadow: 0 8px 18px rgba(15, 23, 42, 0.04);
  align-self: flex-start;
}

.company-avatar {
  width: 52px;
  height: 52px;
  border-radius: 16px;
  background: linear-gradient(135deg, #eef4ff, #dbeafe);
  color: #0d6efd;
  display: grid;
  place-items: center;
  font-weight: 800;
  flex-shrink: 0;
}

.detail-stack {
  display: flex;
  flex-direction: column;
  gap: 0.85rem;
}

.detail-item {
  padding: 0.9rem;
  border: 1px solid #e9ecef;
  border-radius: 14px;
  background: #fff;
}

.detail-label {
  font-size: 0.78rem;
  font-weight: 700;
  color: #6b7280;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  margin-bottom: 0.25rem;
}

.detail-value {
  font-weight: 700;
  color: #111827;
}

.status-box {
  padding: 1rem;
  border: 1px solid #e9ecef;
  border-radius: 16px;
  background: #fff;
}
</style>
