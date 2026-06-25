<template>
  <div class="stat-card">
    <div class="stat-card-row">
      <div class="stat-text">
        <div class="stat-label">{{ title }}</div>
        <div class="stat-value">{{ value }}</div>
        <div v-if="delta" class="stat-delta">
          <i class="ti ti-arrow-up-right"></i>{{ delta }}
        </div>
      </div>

      <div v-if="icon" class="stat-icon">
        <i :class="['ti', icon]"></i>
      </div>
    </div>
  </div>
</template>

<script setup>
defineProps({
  title: String,
  value: [String, Number],
  icon: {
    type: String,
    default: "",
  },
  delta: {
    type: String,
    default: "",
  },
});
</script>

<style scoped>
.stat-card {
  background: white;
  border: 1px solid #e9ecef;
  border-radius: 16px;
  padding: 1rem 1.1rem;
  box-shadow: 0 8px 18px rgba(15, 23, 42, 0.04);
  height: 100%;
}

.stat-card-row {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  gap: 0.75rem;
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

.stat-delta {
  margin-top: 0.4rem;
  font-size: 0.8rem;
  font-weight: 600;
  color: #0d6efd;
  display: flex;
  align-items: center;
  gap: 0.25rem;
}

.stat-icon {
  width: 38px;
  height: 38px;
  border-radius: 10px;
  background: #eef4ff;
  color: #0d6efd;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.1rem;
  flex-shrink: 0;
}
</style>
