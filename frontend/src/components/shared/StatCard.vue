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
  background: linear-gradient(180deg, #ffffff 0%, #fcfdff 100%);
  border: 1px solid #e9eef5;
  border-radius: 18px;
  padding: 1.05rem 1.15rem;
  box-shadow: 0 12px 24px rgba(15, 23, 42, 0.04);
  height: 100%;
}

.stat-card-row {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  gap: 0.9rem;
}

.stat-label {
  font-size: 0.74rem;
  text-transform: uppercase;
  letter-spacing: 0.08em;
  color: #64748b;
  margin-bottom: 0.45rem;
  font-weight: 800;
}

.stat-value {
  font-size: 1.9rem;
  font-weight: 800;
  color: #111827;
  line-height: 1.05;
}

.stat-delta {
  margin-top: 0.45rem;
  font-size: 0.8rem;
  font-weight: 600;
  color: #2563eb;
  display: flex;
  align-items: center;
  gap: 0.25rem;
}

.stat-icon {
  width: 42px;
  height: 42px;
  border-radius: 12px;
  background: linear-gradient(135deg, #e0ecff, #eef4ff);
  color: #0d6efd;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.1rem;
  flex-shrink: 0;
}
</style>
