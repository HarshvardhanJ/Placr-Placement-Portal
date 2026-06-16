<template>
  <PublicLayout>
    <HeroSection />
    <StatsSection />
    <FeaturesSection />
    <HowItWorksSection />
    <section class="py-5 py-lg-6">
      <div class="container">
        <div
          class="card border-0 shadow-lg bg-primary text-white overflow-hidden"
        >
          <div class="card-body p-5 p-lg-6">
            <div class="row align-items-center g-4">
              <div class="col-lg-8">
                <h2 class="fw-bold mb-3">Ready to streamline placements?</h2>
                <p class="mb-0 opacity-75">
                  Create your account and start managing job drives,
                  applications, interviews, and placements in one platform.
                </p>
              </div>
              <div class="col-lg-4 text-lg-end">
                <div
                  class="d-flex flex-column flex-sm-row justify-content-lg-end gap-3"
                >
                  <RouterLink
                    to="/register/student"
                    class="btn btn-light btn-lg"
                  >
                    Student Sign Up
                  </RouterLink>
                  <RouterLink
                    to="/register/company"
                    class="btn btn-outline-light btn-lg"
                  >
                    Company Sign Up
                  </RouterLink>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>
    <PublicFooter />
  </PublicLayout>
</template>

<script setup>
import PublicLayout from "@/layouts/PublicLayout.vue";
import HeroSection from "@/components/public/HeroSection.vue";
import StatsSection from "@/components/public/StatsSection.vue";
import FeaturesSection from "@/components/public/FeaturesSection.vue";
import HowItWorksSection from "@/components/public/HowItWorksSection.vue";
import PublicFooter from "@/components/public/PublicFooter.vue";
</script>
