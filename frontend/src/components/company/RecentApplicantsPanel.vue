<template>
  <div class="card shadow-sm h-100 border-0">
    <div class="card-header bg-white">
      <h5 class="mb-0 fw-semibold">Recent Applicants</h5>
      <small class="text-muted">Latest applications across your drives</small>
    </div>

    <div class="card-body d-flex flex-column gap-3">
      <div
        v-for="applicant in applicants"
        :key="applicant.application_id"
        class="applicant-card p-3 border rounded-3"
      >
        <div class="d-flex align-items-center justify-content-between gap-2">
          <div class="d-flex align-items-center gap-3">
            <div class="avatar">{{ initials(applicant.student_name) }}</div>
            <div>
              <div class="fw-semibold">{{ applicant.student_name }}</div>
              <small class="text-muted">{{ applicant.job_title }}</small>
            </div>
          </div>
          <small class="text-muted text-nowrap">{{ timeAgo(applicant.application_date) }}</small>
        </div>

        <div class="d-flex align-items-center justify-content-between mt-2">
          <span class="badge rounded-pill" :class="statusBadgeClass(applicant.status)">
            {{ applicant.status }}
          </span>

          <div class="d-flex gap-2">
            <RouterLink
              :to="`/company/applications?drive=${applicant.drive_id}&application=${applicant.application_id}`"
              class="btn btn-outline-secondary btn-sm"
            >
              View Profile
            </RouterLink>
          </div>
        </div>
      </div>

      <div v-if="!applicants.length" class="empty-state">
        No applicants yet
      </div>

      <RouterLink
        to="/company/applications"
        class="btn btn-link text-decoration-none fw-semibold mt-auto"
      >
        View All Applicants
      </RouterLink>
    </div>
  </div>
</template>

<script setup>
defineProps({
  applicants: {
    type: Array,
    default: () => [],
  },
});

const initials = (name = "") =>
  String(name)
    .split(" ")
    .filter(Boolean)
    .slice(0, 2)
    .map((part) => part[0]?.toUpperCase())
    .join("") || "ST";

const timeAgo = (value) => {
  if (!value) return "";
  const date = new Date(value);
  if (Number.isNaN(date.getTime())) return "";
  const diff = Math.max(0, Date.now() - date.getTime());
  const mins = Math.floor(diff / 60000);
  if (mins < 1) return "just now";
  if (mins < 60) return `${mins}m ago`;
  const hours = Math.floor(mins / 60);
  if (hours < 24) return `${hours}h ago`;
  const days = Math.floor(hours / 24);
  return `${days}d ago`;
};

const statusBadgeClass = (status = "") => {
  if (status === "shortlisted") return "bg-warning-subtle text-warning-emphasis";
  if (status === "selected") return "bg-success-subtle text-success";
  if (status === "rejected") return "bg-danger-subtle text-danger";
  return "bg-light text-muted border";
};
</script>

<style scoped>
.avatar {
  width: 38px;
  height: 38px;
  border-radius: 10px;
  background: linear-gradient(135deg, #6f42c1, #0d6efd);
  color: white;
  font-weight: 600;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.applicant-card {
  background: #fff;
}

.empty-state {
  padding: 2rem;
  text-align: center;
  color: #6b7280;
}
</style>
