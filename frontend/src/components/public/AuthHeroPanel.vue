<template>
  <div
    class="auth-hero h-100 d-none d-lg-flex flex-column justify-content-center bg-light"
  >
    <div class="auth-hero-inner">
      <h2 class="auth-hero-title fw-bold mb-4">
        Connecting Talent with Opportunity
      </h2>

      <p class="auth-hero-copy lead text-secondary mb-5">
        The modern placement portal engineered to streamline workflows, surface
        insights, and drive meaningful career outcomes for students and
        enterprise partners.
      </p>

      <div class="auth-preview card shadow-sm">
        <div class="card-body text-center">
          <img
            :src="placrLogo"
            alt="PLACR"
            class="auth-preview-logo rounded-3"
          />

          <p class="text-secondary mt-4 mb-0">Placement Dashboard Preview</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import placrLogo from "@/assets/placr.png";
</script>

<style scoped>
.auth-hero {
  padding: clamp(2.5rem, 4.6vh, 4.25rem) clamp(4rem, 6vw, 8rem);
  align-items: center;
}

.auth-hero-inner {
  width: min(100%, 760px);
}

.auth-hero-title {
  max-width: 720px;
  font-size: clamp(3.35rem, 4.1vw, 4.8rem);
  line-height: 1.08;
}

.auth-hero-copy {
  max-width: 740px;
  font-size: 1.12rem;
  line-height: 1.5;
}

.auth-preview {
  width: 100%;
  min-height: 250px;
  border-radius: 0.65rem;
}

.auth-preview .card-body {
  min-height: 250px;
  padding: 2.25rem;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
}

.auth-preview-logo {
  width: 128px;
  height: 128px;
  object-fit: contain;
}

.auth-preview p {
  font-size: 1.05rem;
}
</style>
