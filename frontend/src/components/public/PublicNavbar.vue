<template>
  <nav
    class="navbar navbar-expand-lg bg-body border-bottom sticky-top shadow-sm"
  >
    <div class="container landing-nav-container d-flex align-items-center">
      <RouterLink to="/" class="navbar-brand d-flex align-items-center gap-3">
        <img :src="placrLogo" alt="PLACR" class="brand-logo rounded-3" />
        <div class="d-flex flex-column lh-1">
          <span class="fw-bold text-primary">PLACR</span>
          <small class="text-secondary">Placement Portal</small>
        </div>
      </RouterLink>

      <button
        class="navbar-toggler"
        type="button"
        data-bs-toggle="collapse"
        data-bs-target="#landingNavbar"
        aria-controls="landingNavbar"
        aria-expanded="false"
        aria-label="Toggle navigation"
      >
        <span class="navbar-toggler-icon"></span>
      </button>

      <div class="collapse navbar-collapse" id="landingNavbar">
        <template v-if="!authPage">
          <ul class="navbar-nav mx-auto gap-lg-2 mt-3 mt-lg-0">
            <li class="nav-item">
              <a class="nav-link" href="#features">Features</a>
            </li>
            <li class="nav-item">
              <a class="nav-link" href="#how-it-works">How it works</a>
            </li>
            <li class="nav-item">
              <a class="nav-link" href="#roles">Roles</a>
            </li>
            <li class="nav-item">
              <a class="nav-link" href="#contact">Contact</a>
            </li>
          </ul>

          <div class="d-flex gap-2 mt-3 mt-lg-0">
            <RouterLink to="/login" class="btn btn-outline-primary">
              Sign In
            </RouterLink>

            <RouterLink to="/register" class="btn btn-primary">
              Get Started
            </RouterLink>
          </div>
        </template>

        <template v-else>
          <div class="ms-auto">
            <RouterLink to="/" class="btn btn-outline-primary">
              ← Back Home
            </RouterLink>
          </div>
        </template>
      </div>
    </div>
  </nav>
</template>

<script setup>
import placrLogo from "@/assets/placr.png";
defineProps({
  authPage: {
    type: Boolean,
    default: false,
  },
});
</script>

<style scoped>
.navbar {
  min-height: 96px;
}

.landing-nav-container {
  max-width: 1720px;
  min-height: 96px;
  display: flex;
  align-items: center;
}

.navbar-brand {
  margin-bottom: 0;
  display: flex;
  align-items: center;
}

.brand-logo {
  width: 56px;
  height: 56px;
  object-fit: contain;
}

.navbar-brand span {
  font-size: 1.45rem;
}

.navbar-brand small {
  font-size: 1.18rem;
  font-weight: 600;
}

.nav-link {
  font-size: 1.05rem;
  padding-inline: 1rem !important;
}

.btn {
  --bs-btn-padding-x: 1.25rem;
  --bs-btn-padding-y: 0.65rem;
  --bs-btn-font-size: 1rem;
}

@media (max-width: 991.98px) {
  .navbar,
  .landing-nav-container {
    min-height: 84px;
  }

  .brand-logo {
    width: 48px;
    height: 48px;
  }

  .navbar-brand span {
    font-size: 1.25rem;
  }

  .navbar-brand small {
    font-size: 1rem;
  }
}
</style>
