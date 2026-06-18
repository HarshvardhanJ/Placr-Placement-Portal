<template>
  <div class="card shadow-sm border-0">
    <div class="card-body">
      <p class="text-secondary mb-2">
        {{ title }}
      </p>

      <h2 class="mb-0">
        {{ value }}
      </h2>
    </div>
  </div>
</template>

<script setup>
defineProps({
  title: String,
  value: [String, Number],
  subtitle: String,
  trend: String,
  trendType: String,
  icon: String,
});
</script>
