<template>
  <div class="container py-6">
    <div class="text-center mb-5">
      <h1 class="display-4 fw-bold">Choose Your Account Type</h1>

      <p class="lead text-secondary">Select how you'd like to use PLACR</p>
    </div>

    <div class="row g-5 align-items-stretch">
      <div class="col-lg-5">
        <RoleCard
          title="Student"
          description="Apply to drives, track applications, schedule interviews and manage offers."
          buttonText="Create Student Account"
          to="/register/student"
          :icon="studentIllustration"
        />
      </div>

      <div class="col-lg-2 d-none d-lg-flex justify-content-center">
        <div class="vr h-100" style="min-height: 400px"></div>
      </div>

      <div class="col-lg-5">
        <RoleCard
          title="Company"
          description="Post drives, manage applicants and recruit top talent from campus."
          buttonText="Register Company"
          to="/register/company"
          :icon="companyIllustration"
        />
      </div>
    </div>
  </div>
</template>

<script>
import RoleCard from "@/components/public/RoleCard.vue";
</script>
