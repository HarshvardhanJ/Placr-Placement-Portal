<template>
  <footer id="contact" class="border-top bg-body py-5">
    <div class="container">
      <div class="row g-4">
        <div class="col-lg-4">
          <div class="d-flex align-items-center gap-3 mb-3">
            <img
              :src="placrLogo"
              alt="PLACR"
              class="rounded-3"
              style="width: 40px; height: 40px; object-fit: contain"
            />
            <div class="d-flex flex-column lh-1">
              <span class="fw-bold text-primary">PLACR</span>
              <small class="text-secondary">Placement Portal</small>
            </div>
          </div>
          <p class="text-secondary mb-0">
            The placement portal connecting students, companies, and
            administrators with a modern, transparent workflow.
          </p>
        </div>

        <div class="col-6 col-lg-2">
          <h6 class="fw-semibold mb-3">Product</h6>
          <ul class="list-unstyled text-secondary mb-0">
            <li class="mb-2">
              <a href="#features" class="text-reset text-decoration-none"
                >Features</a
              >
            </li>
            <li class="mb-2">
              <a href="#roles" class="text-reset text-decoration-none">Roles</a>
            </li>
            <li class="mb-2">
              <a href="#how-it-works" class="text-reset text-decoration-none"
                >Workflow</a
              >
            </li>
          </ul>
        </div>

        <div class="col-6 col-lg-2">
          <h6 class="fw-semibold mb-3">Account</h6>
          <ul class="list-unstyled text-secondary mb-0">
            <li class="mb-2">
              <RouterLink to="/login" class="text-reset text-decoration-none">
                Sign In
              </RouterLink>
            </li>
            <li class="mb-2">
              <RouterLink
                to="/register/student"
                class="text-reset text-decoration-none"
              >
                Student Signup
              </RouterLink>
            </li>
            <li class="mb-2">
              <RouterLink
                to="/register/company"
                class="text-reset text-decoration-none"
              >
                Company Signup
              </RouterLink>
            </li>
          </ul>
        </div>

        <div class="col-12 col-lg-4">
          <h6 class="fw-semibold mb-3">
            Built for the campus placement process
          </h6>
        </div>
      </div>

      <div
        class="d-flex flex-column flex-md-row justify-content-between align-items-center gap-3 pt-4 mt-4 border-top"
      >
        <small class="text-secondary">© 2026 PLACR. All rights reserved.</small>
        <small class="text-secondary">Made for campus placements</small>
      </div>
    </div>
  </footer>
</template>

<script setup>
import placrLogo from "@/assets/placr.png";
</script>
