<template>
  <div
    class="auth-hero h-100 d-none d-lg-flex flex-column justify-content-center"
    :style="{ backgroundImage: `linear-gradient(90deg, rgba(7, 13, 28, 0.84), rgba(15, 23, 42, 0.56)), url(${heroImage})` }"
  >
    <div class="auth-hero-inner">
      <div class="hero-kicker mb-3">
        <i class="ti ti-chart-line"></i>
        <span>Placement intelligence workspace</span>
      </div>

      <h2 class="auth-hero-title fw-bold mb-4">
        Connecting Talent<br />
        with Opportunity
      </h2>

      <p class="auth-hero-copy mb-4">
        The modern placement portal engineered to streamline workflows, surface
        insights, and drive meaningful career outcomes for students and
        enterprise partners.
      </p>

      <div class="hero-feature-grid">
        <div v-for="feature in features" :key="feature.title" class="hero-feature">
          <i :class="['ti', feature.icon]"></i>
          <div>
            <div class="hero-feature-title">{{ feature.title }}</div>
            <div class="hero-feature-copy">{{ feature.copy }}</div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import heroImage from "@/assets/placement-hero.jpg";

const features = [
  {
    title: "Eligibility Matching",
    copy: "Intelligent eligibility filtering so students only see placement opportunities they qualify for.",
    icon: "ti-filter-check",
  },
  {
    title: "Recruitment Workflow",
    copy: "Complete hiring pipeline from job posting to final offer acceptance.",
    icon: "ti-route",
  },
  {
    title: "Analytics & Reports",
    copy: "Placement insights, application tracking, and export-ready reports for administrators and recruiters.",
    icon: "ti-report-analytics",
  },
];
</script>

<style scoped>
.auth-hero {
  padding: clamp(2.5rem, 4.6vh, 4.25rem) clamp(4rem, 6vw, 8rem);
  align-items: center;
  background-size: cover;
  background-position: center;
  position: relative;
  isolation: isolate;
}

.auth-hero::after {
  content: "";
  position: absolute;
  inset: 0;
  background:
    radial-gradient(circle at 20% 15%, rgba(59, 130, 246, 0.25), transparent 28%),
    linear-gradient(180deg, rgba(15, 23, 42, 0), rgba(15, 23, 42, 0.35));
  pointer-events: none;
  z-index: 0;
}

.auth-hero-inner {
  width: min(100%, 760px);
  position: relative;
  z-index: 1;
}

.auth-hero-title {
  max-width: 720px;
  font-size: clamp(3rem, 3.8vw, 4.3rem);
  line-height: 1.05;
  color: #ffffff;
}

.auth-hero-copy {
  max-width: 680px;
  font-size: 1.08rem;
  line-height: 1.55;
  color: rgba(255, 255, 255, 0.82);
}

.hero-kicker {
  align-self: flex-start;
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.55rem 0.9rem;
  border-radius: 999px;
  background: rgba(255, 255, 255, 0.16);
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.2);
  color: #ffffff;
  font-size: 0.92rem;
  font-weight: 600;
}

.hero-feature-grid {
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: 1rem;
  margin-top: 2rem;
}

.hero-feature {
  min-height: 132px;
  border-radius: 1rem;
  padding: 1rem;
  background: rgba(255, 255, 255, 0.14);
  border: 1px solid rgba(255, 255, 255, 0.2);
  backdrop-filter: blur(14px);
  color: #ffffff;
}

.hero-feature i {
  font-size: 1.45rem;
  margin-bottom: 0.85rem;
  color: #bfdbfe;
}

.hero-feature-title {
  font-weight: 800;
  margin-bottom: 0.3rem;
}

.hero-feature-copy {
  color: rgba(255, 255, 255, 0.75);
  font-size: 0.92rem;
  line-height: 1.35;
}

@media (max-width: 1199.98px) {
  .auth-hero {
    padding: 2.25rem 2rem;
  }

  .hero-feature-grid {
    grid-template-columns: 1fr;
  }
}

@media (max-width: 991.98px) {
  .auth-hero {
    padding: 1.5rem;
  }
}
</style>
