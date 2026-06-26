<template>
  <div class="card shadow-sm border-0 h-100">
    <div class="card-body">
      <div class="d-flex justify-content-between align-items-start gap-2 mb-3">
        <div>
          <h6 class="mb-1 fw-semibold">Upcoming Actions</h6>
          <small class="text-muted">Interviews, deadlines, and reminders</small>
        </div>
        <i class="ti ti-bell text-primary"></i>
      </div>

      <div class="action-stack">
        <div v-if="upcomingInterviews.length" class="action-item action-highlight">
          <div class="d-flex justify-content-between gap-2">
            <div>
              <div class="fw-semibold">Interview scheduled</div>
              <small class="text-muted">{{ upcomingInterviews[0].company }} · {{ upcomingInterviews[0].job_title }}</small>
            </div>
            <span class="badge text-bg-primary">Soon</span>
          </div>
          <div class="mt-2 small text-muted">
            {{ formatDate(upcomingInterviews[0].interview_date) }}
            <span v-if="upcomingInterviews[0].interview_type">
              · {{ upcomingInterviews[0].interview_type }}
            </span>
          </div>
        </div>

        <div class="action-item">
          <div class="fw-semibold">Complete profile</div>
          <small class="text-muted">Keep education, CGPA, and skills updated.</small>
        </div>

        <div class="action-item">
          <div class="fw-semibold">Review application deadlines</div>
          <small class="text-muted">Check drives before they close.</small>
        </div>

        <div v-if="nextDeadline" class="action-item">
          <div class="fw-semibold">Next deadline</div>
          <small class="text-muted">{{ nextDeadline }}</small>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed } from "vue";

const props = defineProps({
  upcomingInterviews: {
    type: Array,
    default: () => [],
  },
  eligibleDrives: {
    type: Array,
    default: () => [],
  },
});

const nextDeadline = computed(() => {
  const drive = props.eligibleDrives[0];
  if (!drive) return "";
  const value = drive.application_deadline || drive.deadline;
  if (!value) return "";
  return formatDate(value);
});

const formatDate = (value) => {
  if (!value) return "";
  const date = new Date(value);
  if (Number.isNaN(date.getTime())) return String(value);

  return date.toLocaleString("en-IN", {
    day: "numeric",
    month: "short",
    hour: "numeric",
    minute: "2-digit",
  });
};
</script>

<style scoped>
.action-stack {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}

.action-item {
  padding: 0.9rem;
  border: 1px solid #e9ecef;
  border-radius: 14px;
  background: #f8fafc;
}

.action-highlight {
  background: #eef4ff;
  border-color: #dbeafe;
}
</style>
