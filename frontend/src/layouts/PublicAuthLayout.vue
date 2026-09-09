<template>
  <div class="auth-shell d-flex flex-column">
    <PublicNavbar :auth-page="true" />
    <main class="auth-main flex-grow-1">
      <div class="container-fluid p-0 h-100">
        <div class="auth-row row g-0 h-100">
          <div class="auth-column col-lg-6 h-100">
            <AuthHeroPanel />
          </div>

          <div class="auth-column col-lg-6 h-100 auth-form-side">
            <slot />
          </div>
        </div>
      </div>
    </main>
  </div>
</template>

<script setup>
import PublicNavbar from "@/components/public/PublicNavbar.vue";
import AuthHeroPanel from "@/components/public/AuthHeroPanel.vue";
</script>

<style scoped>
.auth-shell {
  min-height: 100vh;
}

.auth-main {
  height: calc(100vh - 112px);
  min-height: 0;
  overflow: hidden;
  background: #ffffff;
}

.auth-main > .container-fluid,
.auth-row,
.auth-column {
  min-height: 100%;
}

.auth-form-side {
  background: #fff;
}

@media (max-width: 991.98px) {
  .auth-main {
    height: auto;
    min-height: calc(100vh - 100px);
    overflow: visible;
  }

  .auth-row,
  .auth-column {
    min-height: inherit;
  }
}
</style>
