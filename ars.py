c = 0.1
a = 10

def formula(c, t, r, a):
    return c * t**2 * r + a

def calculate_volunteer(organization_rep, time_volunteered):
    return formula(c, time_volunteered, organization_rep, a)

def calculate_organization(volunteer_rep):
    return formula(c, 1, volunteer_rep, a)
