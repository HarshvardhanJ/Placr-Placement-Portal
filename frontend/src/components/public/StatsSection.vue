<template>
  <section class="py-4 py-lg-5 border-top border-bottom bg-body">
    <div class="container">
      <div class="row g-3">
        <div v-for="item in stats" :key="item.label" class="col-6 col-lg-3">
          <div class="card border-0 shadow-sm h-100">
            <div class="card-body text-center py-4">
              <div class="fs-2 fw-bold text-primary mb-1">
                {{ item.value }}
              </div>
              <div class="text-secondary small text-uppercase tracking-wide">
                {{ item.label }}
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </section>
</template>

<script setup>
const stats = [
  { value: "500+", label: "Students" },
  { value: "100+", label: "Companies" },
  { value: "300+", label: "Drives" },
  { value: "95%", label: "Success Rate" },
];
</script>

<style scoped>
.tracking-wide {
  letter-spacing: 0.08em;
}
</style>
