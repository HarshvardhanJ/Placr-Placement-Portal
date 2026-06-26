<template>
  <div class="drive-card card shadow-sm border-0 h-100">
    <div class="card-body p-3 p-lg-4">
      <div class="d-flex justify-content-between gap-3">
        <div class="d-flex gap-3">
          <div class="company-logo">{{ initials }}</div>

          <div>
            <h5 class="mb-1 fw-semibold">{{ drive.job_title }}</h5>
            <div class="text-muted small d-flex flex-wrap align-items-center gap-2">
              <span>{{ drive.company_name || drive.company?.name || "Company" }}</span>
              <span v-if="drive.job_location">• {{ drive.job_location }}</span>
              <span v-if="drive.job_type">• {{ drive.job_type }}</span>
            </div>

            <div class="d-flex flex-wrap gap-2 mt-3">
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

        <button class="bookmark-btn" type="button" title="Save drive">
          <i class="ti ti-bookmark"></i>
        </button>
      </div>

      <div class="drive-meta row g-2 mt-3">
        <div class="col-auto">
          <span class="meta-item"><i class="ti ti-calendar-event me-1"></i>{{ deadlineLabel }}</span>
        </div>
        <div class="col-auto">
          <span class="meta-item"><i class="ti ti-wallet me-1"></i>{{ salaryLabel }}</span>
        </div>
        <div class="col-auto">
          <span class="meta-item"><i class="ti ti-user-check me-1"></i>{{ eligibilityLabel }}</span>
        </div>
      </div>

      <div class="d-flex flex-wrap gap-2 mt-4">
        <RouterLink :to="`/student/drives/${drive.drive_id}`" class="btn btn-outline-primary btn-sm">
          View Details
        </RouterLink>
        <button type="button" class="btn btn-primary btn-sm" :disabled="disabled">
          {{ actionLabel }}
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed } from "vue";

const props = defineProps({
  drive: {
    type: Object,
    required: true,
  },
  disabled: {
    type: Boolean,
    default: false,
  },
  actionLabel: {
    type: String,
    default: "Apply Now",
  },
});

const initials = computed(() => {
  const value = props.drive.company_name || props.drive.company?.name || "DR";
  return (
    value
      .split(" ")
      .filter(Boolean)
      .slice(0, 2)
      .map((part) => part[0]?.toUpperCase())
      .join("") || "DR"
  );
});

const skillTags = computed(() => {
  const raw = props.drive.required_skills || props.drive.skills_required || "";
  return raw
    .split(",")
    .map((item) => item.trim())
    .filter(Boolean)
    .slice(0, 4);
});

const deadlineLabel = computed(() => {
  const value = props.drive.application_deadline || props.drive.deadline;
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
  const min = props.drive.salary_min ?? props.drive.min_salary;
  const max = props.drive.salary_max ?? props.drive.max_salary;
  if (min && max) return `₹${min} - ₹${max}`;
  if (min) return `From ₹${min}`;
  if (max) return `Up to ₹${max}`;
  return "Salary on request";
});

const eligibilityLabel = computed(() => {
  if (props.drive.year) return `Year ${props.drive.year}`;
  if (props.drive.min_cgpa) return `Min CGPA ${props.drive.min_cgpa}`;
  return "Open eligibility";
});
</script>

<style scoped>
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

.bookmark-btn {
  width: 36px;
  height: 36px;
  border-radius: 10px;
  border: 1px solid #e9ecef;
  background: #fff;
  color: #6b7280;
  display: grid;
  place-items: center;
  flex-shrink: 0;
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

.drive-card {
  border-radius: 1rem;
}
</style>
