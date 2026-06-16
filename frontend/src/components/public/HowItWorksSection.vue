<template>
  <section
    id="how-it-works"
    class="py-5 py-lg-6 bg-body-tertiary border-top border-bottom"
  >
    <div class="container">
      <div class="text-center mb-5">
        <h2 class="fw-bold mb-3">How it works</h2>
        <p class="text-secondary mx-auto" style="max-width: 720px">
          A simple placement flow from registration to offer letter.
        </p>
      </div>

      <div class="row g-4">
        <div class="col-md-3" v-for="(step, index) in steps" :key="step.title">
          <div class="card h-100 border-0 shadow-sm step-card text-center">
            <div class="card-body p-4">
              <div class="step-number mx-auto mb-3">{{ index + 1 }}</div>
              <h5 class="fw-semibold">{{ step.title }}</h5>
              <p class="text-secondary mb-0">{{ step.description }}</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  </section>
</template>

<script setup>
const steps = [
  {
    title: "Create account",
    description:
      "Register as a student or company and start with role-based access.",
  },
  {
    title: "Complete profile",
    description:
      "Add the required details, resume, and eligibility information.",
  },
  {
    title: "Apply or post",
    description:
      "Students apply to drives while companies post and manage openings.",
  },
  {
    title: "Get placed",
    description: "Track interviews, selection, and offer letter delivery.",
  },
];
</script>

<style scoped>
.step-card {
  transition:
    transform 0.2s ease,
    box-shadow 0.2s ease;
}

.step-card:hover {
  transform: translateY(-4px);
}

.step-number {
  width: 2.75rem;
  height: 2.75rem;
  border-radius: 9999px;
  background: #2563eb;
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 700;
}
</style>
