<template>
  <div class="card h-100 shadow-sm border-0 role-card">
    <div class="card-body text-center p-5">
      <div class="mb-4">
        <img :src="icon" :alt="title" width="120" height="120" />
      </div>

      <h2 class="fw-bold mb-3">
        {{ title }}
      </h2>

      <p class="text-secondary mb-4">
        {{ description }}
      </p>

      <RouterLink :to="to" class="btn btn-primary px-4">
        {{ buttonText }}
      </RouterLink>
    </div>
  </div>
</template>

<script setup>
defineProps({
  title: String,
  description: String,
  buttonText: String,
  to: String,
  icon: String,
});
</script>

<style scoped>
.role-card {
  transition: all 0.2s ease;
}

.role-card:hover {
  transform: translateY(-4px);
}
</style>
