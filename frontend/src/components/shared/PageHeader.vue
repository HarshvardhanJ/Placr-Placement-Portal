<template>
  <div
    class="d-flex flex-column flex-lg-row justify-content-between align-items-lg-center gap-3 mb-4"
  >
    <div>
      <h2 class="mb-1 fw-bold">{{ title }}</h2>

      <p class="text-secondary mb-0">
        {{ subtitle }}
      </p>
    </div>

    <div v-if="$slots.actions" class="page-header-actions">
      <slot name="actions" />
    </div>
  </div>
</template>

<script setup>
defineProps({
  title: String,
  subtitle: String,

  showExport: {
    type: Boolean,
    default: false,
  },

  showCreate: {
    type: Boolean,
    default: false,
  },
});
</script>

<style scoped>
.page-header {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  gap: 1rem;
  margin-bottom: 1.5rem;
}

.page-header-text {
  min-width: 0;
}

.page-title {
  margin: 0;
  font-size: 1.6rem;
  font-weight: 800;
  letter-spacing: -0.03em;
  color: #1f2937;
  line-height: 1.2;
}

.page-subtitle {
  margin: 0.35rem 0 0;
  color: #6b7280;
  font-size: 0.95rem;
  line-height: 1.5;
}

.page-header-actions {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  flex-shrink: 0;
}

@media (max-width: 991.98px) {
  .page-header {
    flex-direction: column;
    align-items: stretch;
  }

  .page-header-actions {
    justify-content: flex-start;
  }
}
</style>
