<template>
  <div class="card shadow-sm h-100 border-0 rounded-4 overflow-hidden">
    <div class="card-header bg-white border-bottom-0 px-4 pt-4 pb-3">
      <h5 class="mb-0 fw-semibold">
        {{ title }}
      </h5>
    </div>

    <div class="card-body p-0">
      <div v-if="items.length">
        <div v-for="item in items" :key="item.title" class="action-item">
          <div style="min-width: 0">
            <div class="fw-semibold text-truncate">
              {{ item.title }}
            </div>

            <small class="text-secondary text-truncate d-block">
              {{ item.subtitle }}
            </small>
          </div>

          <RouterLink
            :to="item.link"
            class="btn btn-sm btn-outline-primary flex-shrink-0"
          >
            View
          </RouterLink>
        </div>
      </div>

      <div v-else class="empty-state">
        <i class="ti ti-check text-success fs-3 mb-2"></i>
        <div class="fw-semibold">No pending actions</div>
      </div>
    </div>
  </div>
</template>

<script setup>
defineProps({
  title: String,
  items: {
    type: Array,
    default: () => [],
  },
});
</script>

<style scoped>
.action-item {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 1rem;
  padding: 1rem 1.25rem;
  border-bottom: 1px solid #eef2f7;
}

.action-item:last-child {
  border-bottom: none;
}

.empty-state {
  min-height: 170px;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  color: #6b7280;
}
</style>
