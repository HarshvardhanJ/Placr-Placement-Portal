<template>
  <section class="landing-hero position-relative overflow-hidden">
    <div class="hero-blob"></div>

    <div class="container hero-container">
      <div class="row align-items-center g-5 g-xl-6">
        <div class="col-lg-6">
          <span
            class="hero-eyebrow badge rounded-pill text-bg-primary-subtle text-primary border border-primary-subtle px-3 py-2 mb-4"
          >
            The future of campus placements
          </span>

          <h1 class="hero-title fw-bold lh-1 mb-4">
            Connecting Talent with
            <span class="text-primary">Opportunity</span>
          </h1>

          <p class="hero-copy lead text-secondary mb-4">
            A centralized platform for students, recruiters, and placement cells
            to manage recruitment efficiently. Discover drives, track
            applications, schedule interviews, and manage offers from one place.
          </p>

          <div class="hero-actions d-flex flex-column flex-sm-row gap-3">
            <RouterLink
              to="/register/student"
              class="btn btn-primary btn-lg px-4"
            >
              Get Started
            </RouterLink>
            <a href="#features" class="btn btn-outline-primary btn-lg px-4">
              Explore Features
            </a>
          </div>

          <div class="hero-points d-flex flex-wrap gap-3 mt-4">
            <div class="d-flex align-items-center gap-2 text-secondary">
              <span
                class="badge rounded-pill text-bg-success-subtle text-success border border-success-subtle"
                >●</span
              >
              Role-based access
            </div>
            <div class="d-flex align-items-center gap-2 text-secondary">
              <span
                class="badge rounded-pill text-bg-info-subtle text-info border border-info-subtle"
                >●</span
              >
              Interview tracking
            </div>
            <div class="d-flex align-items-center gap-2 text-secondary">
              <span
                class="badge rounded-pill text-bg-warning-subtle text-warning border border-warning-subtle"
                >●</span
              >
              Offer management
            </div>
          </div>
        </div>

        <div class="col-lg-6">
          <div class="card border-0 shadow-lg dashboard-card overflow-hidden">
            <div
              class="card-header bg-body d-flex align-items-center justify-content-between py-3"
            >
              <div>
                <div class="fw-semibold">Dashboard preview</div>
                <small class="text-secondary"
                  >A quick look at the student experience</small
                >
              </div>
              <span
                class="badge text-bg-primary-subtle text-primary border border-primary-subtle"
              >
                Live UI
              </span>
            </div>

            <div class="card-body dashboard-body">
              <div class="row g-3">
                <div class="col-6">
                  <div
                    class="card stat-card border-0 bg-primary text-white h-100"
                  >
                    <div class="card-body">
                      <div class="fs-2 fw-bold">12</div>
                      <div class="opacity-75">Eligible Drives</div>
                    </div>
                  </div>
                </div>

                <div class="col-6">
                  <div
                    class="card stat-card border-0 bg-success text-white h-100"
                  >
                    <div class="card-body">
                      <div class="fs-2 fw-bold">4</div>
                      <div class="opacity-75">Applications</div>
                    </div>
                  </div>
                </div>

                <div class="col-6">
                  <div
                    class="card stat-card border-0 bg-warning text-dark h-100"
                  >
                    <div class="card-body">
                      <div class="fs-2 fw-bold">2</div>
                      <div class="opacity-75">Shortlisted</div>
                    </div>
                  </div>
                </div>

                <div class="col-6">
                  <div class="card stat-card border-0 bg-dark text-white h-100">
                    <div class="card-body">
                      <div class="fs-2 fw-bold">1</div>
                      <div class="opacity-75">Placements</div>
                    </div>
                  </div>
                </div>
              </div>

              <div class="mt-4">
                <div
                  class="d-flex align-items-center justify-content-between mb-3"
                >
                  <h5 class="mb-0">Recent drives</h5>
                  <a href="#" class="text-decoration-none small">View all</a>
                </div>

                <div
                  class="list-group list-group-flush border rounded-3 overflow-hidden"
                >
                  <div
                    class="list-group-item d-flex justify-content-between align-items-center py-3"
                  >
                    <div>
                      <div class="fw-semibold">Google</div>
                      <small class="text-secondary"
                        >Software Engineer • 20 LPA</small
                      >
                    </div>
                    <span class="badge bg-success">Apply</span>
                  </div>

                  <div
                    class="list-group-item d-flex justify-content-between align-items-center py-3"
                  >
                    <div>
                      <div class="fw-semibold">Amazon</div>
                      <small class="text-secondary"
                        >Backend Intern • 12 LPA</small
                      >
                    </div>
                    <span class="badge bg-primary">Open</span>
                  </div>

                  <div
                    class="list-group-item d-flex justify-content-between align-items-center py-3"
                  >
                    <div>
                      <div class="fw-semibold">Microsoft</div>
                      <small class="text-secondary">SDE • 22 LPA</small>
                    </div>
                    <span class="badge bg-warning text-dark"
                      >Deadline Soon</span
                    >
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </section>
</template>

<style scoped>
.landing-hero {
  min-height: calc(100vh - 96px);
  padding-block: clamp(3.5rem, 6vh, 6rem);
  display: flex;
  align-items: center;
}

.hero-container {
  max-width: 1720px;
}

.hero-blob {
  position: absolute;
  top: -10rem;
  right: -12rem;
  width: 36rem;
  height: 36rem;
  border-radius: 9999px;
  background: radial-gradient(
    circle,
    rgba(37, 99, 235, 0.14) 0%,
    rgba(124, 58, 237, 0.08) 42%,
    rgba(248, 250, 252, 0) 70%
  );
  filter: blur(14px);
  pointer-events: none;
}

.hero-eyebrow {
  font-size: 1rem;
  font-weight: 500;
  letter-spacing: 0;
}

.hero-title {
  max-width: 780px;
  font-size: clamp(4.25rem, 5.8vw, 6.6rem);
}

.hero-copy {
  max-width: 850px;
  font-size: 1.28rem;
  line-height: 1.5;
}

.hero-actions .btn {
  min-height: 64px;
  min-width: 178px;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  font-size: 1.12rem;
}

.hero-points {
  font-size: 1.08rem;
}

.dashboard-card {
  min-height: 655px;
  border-radius: 0.65rem;
}

.dashboard-card .card-header {
  padding: 1.6rem 1.9rem !important;
}

.dashboard-card .card-header .fw-semibold {
  font-size: 1.2rem;
}

.dashboard-card .card-header small,
.dashboard-card .list-group-item small {
  font-size: 1rem;
}

.dashboard-card .badge {
  font-size: 0.95rem;
}

.dashboard-body {
  padding: 2rem;
}

.stat-card {
  min-height: 160px;
  border-radius: 0.55rem;
}

.stat-card .card-body {
  padding: 1.65rem 1.75rem;
}

.stat-card .fs-2 {
  font-size: 2.25rem !important;
}

.stat-card .opacity-75 {
  font-size: 1.12rem;
}

.dashboard-card h5 {
  font-size: 1.08rem;
}

.dashboard-card .list-group-item {
  min-height: 84px;
  padding-inline: 1.75rem;
}

.dashboard-card .list-group-item .fw-semibold {
  font-size: 1.08rem;
}

@media (max-width: 1199.98px) {
  .hero-title {
    font-size: clamp(3.6rem, 6.8vw, 5.4rem);
  }

  .dashboard-card {
    min-height: 610px;
  }
}

@media (max-width: 991.98px) {
  .landing-hero {
    min-height: auto;
    padding-block: 4rem;
  }

  .hero-title {
    max-width: none;
    font-size: clamp(3.2rem, 10vw, 4.4rem);
  }

  .hero-copy {
    font-size: 1.15rem;
  }
}

@media (max-width: 575.98px) {
  .landing-hero {
    padding-block: 2.75rem;
  }

  .hero-title {
    font-size: clamp(2.75rem, 13vw, 3.4rem);
  }

  .hero-actions .btn {
    width: 100%;
  }

  .dashboard-body {
    padding: 1.25rem;
  }

  .stat-card {
    min-height: 132px;
  }

  .dashboard-card .list-group-item {
    padding-inline: 1rem;
  }
}
</style>
