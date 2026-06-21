<template>
  <div class="card shadow-sm">
    <div class="card-header">
      <h3 class="card-title">
        {{ title }}
      </h3>
    </div>

    <div class="card-body">
      <div v-if="activities.length">
        <div
          v-for="activity in activities"
          :key="activity.message"
          class="d-flex gap-3 mb-3"
        >
          <div
            class="rounded-circle flex-shrink-0"
            :class="`bg-${activity.color}`"
            style="width: 10px; height: 10px; margin-top: 8px"
          />

          <div>
            <div class="fw-medium">
              {{ activity.message }}
            </div>

            <small class="text-secondary">
              {{ activity.time }}
            </small>
          </div>
        </div>
      </div>
      <div v-else class="empty-state">No recent activity</div>
    </div>
  </div>
</template>

<script setup>
defineProps({
  title: {
    type: String,
    default: "Recent Activity",
  },

  activities: {
    type: Array,
    default: () => [],
  },
});
</script>

<style scoped>
.empty-state {
  padding: 2rem;
  text-align: center;
  color: #6c757d;
  font-size: 0.95rem;
}
</style>
