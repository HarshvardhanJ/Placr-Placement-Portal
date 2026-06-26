<template>
  <div class="student-empty-state">
    <i :class="['ti', icon, 'empty-icon']"></i>
    <div class="fw-semibold mb-1">{{ title }}</div>
    <small class="text-muted">{{ subtitle }}</small>

    <div v-if="$slots.actions" class="mt-3">
      <slot name="actions" />
    </div>
  </div>
</template>

<script setup>
defineProps({
  icon: {
    type: String,
    default: "ti-layout-dashboard-off",
  },
  title: {
    type: String,
    default: "Nothing here yet",
  },
  subtitle: {
    type: String,
    default: "This section will populate when data becomes available.",
  },
});
</script>

<style scoped>
.student-empty-state {
  min-height: 220px;
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
</style>
