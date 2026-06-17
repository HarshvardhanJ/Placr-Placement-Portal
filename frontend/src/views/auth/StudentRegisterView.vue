<template>
  <div class="auth-shell d-flex flex-column">
    <PublicNavbar :auth-page="true" />
    <main class="auth-main d-flex flex-grow-1 bg-white">
      <StudentRegistrationFormCard />
    </main>
  </div>
</template>

<script setup>
import PublicNavbar from "@/components/public/PublicNavbar.vue";
import StudentRegistrationFormCard from "@/components/public/StudentRegistrationFormCard.vue";
</script>

<style scoped>
.auth-shell {
  min-height: 100vh;
}

.auth-main {
  min-height: 0;
}
</style>
