<template>
  <section id="features" class="py-5 py-lg-6">
    <div class="container">
      <div class="text-center mb-5">
        <span
          class="badge rounded-pill text-bg-primary-subtle text-primary border border-primary-subtle px-3 py-2 mb-3"
        >
          Built for the placement ecosystem
        </span>
        <h2 class="fw-bold mb-3">
          Designed for students, recruiters, and administrators
        </h2>
        <p class="text-secondary mx-auto" style="max-width: 760px">
          PLACR gives each role exactly what it needs: a clean student
          experience, a powerful recruiter workflow, and a transparent admin
          control panel.
        </p>
      </div>

      <div class="row g-4" id="roles">
        <div class="col-md-4" v-for="role in roles" :key="role.title">
          <div class="card h-100 border-0 shadow-sm feature-card">
            <div class="card-body p-4">
              <div class="icon-badge mb-4" :class="role.iconBg">
                <span class="fw-bold">{{ role.short }}</span>
              </div>

              <h4 class="fw-semibold mb-2">{{ role.title }}</h4>
              <p class="text-secondary mb-4">{{ role.description }}</p>

              <ul class="list-unstyled mb-0">
                <li
                  v-for="point in role.points"
                  :key="point"
                  class="d-flex align-items-start gap-2 mb-3"
                >
                  <span class="text-success mt-1">✓</span>
                  <span class="text-secondary">{{ point }}</span>
                </li>
              </ul>
            </div>
          </div>
        </div>
      </div>
    </div>
  </section>
</template>

<script setup>
const roles = [
  {
    short: "S",
    title: "For Students",
    description:
      "Browse drives, apply to jobs, track interviews, and download offer letters from one dashboard.",
    iconBg: "icon-blue",
    points: [
      "Discover relevant placement drives",
      "Track application status and interviews",
      "Manage profile, resume, and placements",
    ],
  },
  {
    short: "C",
    title: "For Companies",
    description:
      "Post jobs, review applicants, schedule interviews, and manage placement decisions efficiently.",
    iconBg: "icon-green",
    points: [
      "Create and close placement drives",
      "Shortlist or reject applicants",
      "Upload offer letters and placement details",
    ],
  },
  {
    short: "A",
    title: "For Admins",
    description:
      "Oversee approvals, manage users, and keep the placement ecosystem organized and transparent.",
    iconBg: "icon-purple",
    points: [
      "Approve companies and drives",
      "Search students and companies",
      "Monitor platform activity and records",
    ],
  },
];
</script>

<style scoped>
.feature-card {
  transition:
    transform 0.2s ease,
    box-shadow 0.2s ease;
}

.feature-card:hover {
  transform: translateY(-4px);
}

.icon-badge {
  width: 3rem;
  height: 3rem;
  border-radius: 9999px;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  font-weight: 700;
}

.icon-blue {
  background: rgba(37, 99, 235, 0.1);
  color: #2563eb;
}

.icon-green {
  background: rgba(22, 163, 74, 0.1);
  color: #16a34a;
}

.icon-purple {
  background: rgba(124, 58, 237, 0.1);
  color: #7c3aed;
}
</style>
