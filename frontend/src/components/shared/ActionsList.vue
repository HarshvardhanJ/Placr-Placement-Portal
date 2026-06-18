<template>
  <div class="card shadow-sm h-100">
    <div class="card-header">
      <h3 class="card-title">
        {{ title }}
      </h3>
    </div>

    <div class="card-body">
      <div
        v-for="item in items"
        :key="item.title"
        class="d-flex justify-content-between align-items-center py-3 border-bottom"
      >
        <div>
          <div class="fw-medium">
            {{ item.title }}
          </div>

          <small class="text-secondary">
            {{ item.subtitle }}
          </small>
        </div>

        <div class="d-flex gap-2">
          <button class="btn btn-sm btn-success">Approve</button>

          <button class="btn btn-sm btn-outline-danger">Reject</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
defineProps({
  title: String,
  items: Array,
});
</script>
