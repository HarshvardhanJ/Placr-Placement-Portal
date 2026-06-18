<template>
  <aside class="sidebar">
    <div class="sidebar-brand">
      <h3>PLACR</h3>
      <small>Admin Panel</small>
    </div>

    <nav>
      <RouterLink to="/admin" class="sidebar-link"> Dashboard </RouterLink>

      <RouterLink to="/admin/companies" class="sidebar-link">
        Companies
      </RouterLink>

      <RouterLink to="/admin/students" class="sidebar-link">
        Students
      </RouterLink>

      <RouterLink to="/admin/drives" class="sidebar-link"> Drives </RouterLink>

      <RouterLink to="/admin/applications" class="sidebar-link">
        Applications
      </RouterLink>
    </nav>
  </aside>
</template>

<style scoped>
.sidebar {
  width: 260px;
  background: white;
  border-right: 1px solid #dee2e6;
  padding: 1rem;
}

.sidebar-brand {
  margin-bottom: 2rem;
}

.sidebar-link {
  display: block;
  padding: 0.75rem;
  color: #495057;
  text-decoration: none;
  border-radius: 8px;
}

.sidebar-link:hover {
  background: #f1f3f5;
}

.router-link-active {
  background: #0d6efd;
  color: white;
}
</style>
