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

    <div class="d-flex gap-2">
      <slot name="actions"></slot>
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
