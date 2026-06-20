<template>
  <div class="stat-card">
    <div class="stat-label">{{ title }}</div>
    <div class="stat-value">{{ value }}</div>
  </div>
</template>

<script setup>
defineProps({
  title: String,
  value: [String, Number],
});
</script>

<style scoped>
.stat-card {
  background: white;
  border: 1px solid #e9ecef;
  border-radius: 16px;
  padding: 1rem 1.1rem;
  box-shadow: 0 8px 18px rgba(15, 23, 42, 0.04);
}

.stat-label {
  font-size: 0.8rem;
  text-transform: uppercase;
  letter-spacing: 0.06em;
  color: #6b7280;
  margin-bottom: 0.35rem;
  font-weight: 700;
}

.stat-value {
  font-size: 1.6rem;
  font-weight: 800;
  color: #1f2937;
  line-height: 1.1;
}
</style>
