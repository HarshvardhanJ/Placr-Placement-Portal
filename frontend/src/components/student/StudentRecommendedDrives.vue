<template>
  <div class="card shadow-sm border-0 h-100">
    <div class="card-body">
      <div class="d-flex align-items-start justify-content-between gap-3 mb-3">
        <div>
          <h6 class="mb-1 fw-semibold">Recommended Job Drives</h6>
          <small class="text-muted">Matched to your profile and eligibility</small>
        </div>
        <RouterLink to="/student/drives" class="btn btn-link btn-sm text-decoration-none">
          View All
        </RouterLink>
      </div>

      <div v-if="loading" class="text-center py-5 text-muted">
        Loading drives...
      </div>

      <template v-else-if="drives.length">
        <div class="drive-stack">
          <StudentDriveCard
            v-for="drive in drives.slice(0, 2)"
            :key="drive.drive_id"
            :drive="drive"
          />
        </div>
      </template>

      <StudentEmptyState
        v-else
        icon="ti-briefcase-off"
        title="No drives available"
        subtitle="Eligible drives will appear here once companies post and admin approves them."
      >
        <template #actions>
          <RouterLink to="/student/drives" class="btn btn-outline-primary btn-sm">
            Browse Drives
          </RouterLink>
        </template>
      </StudentEmptyState>
    </div>
  </div>
</template>

<script setup>
import StudentDriveCard from "./StudentDriveCard.vue";
import StudentEmptyState from "./StudentEmptyState.vue";

defineProps({
  drives: {
    type: Array,
    default: () => [],
  },
  loading: {
    type: Boolean,
    default: false,
  },
});
</script>

<style scoped>
.drive-stack {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}
</style>
