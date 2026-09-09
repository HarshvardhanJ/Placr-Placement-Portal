<template>
  <div class="min-vh-80 bg-body-tertiary d-flex flex-column">
    <PublicNavbar />
    <main class="flex-grow-1">
      <slot />
    </main>
  </div>
</template>

<script setup>
import PublicNavbar from "@/components/public/PublicNavbar.vue";
</script>
