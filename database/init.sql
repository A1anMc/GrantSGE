-- Enable necessary extensions
create extension if not exists "uuid-ossp";
create extension if not exists "pgcrypto";

-- Create custom types
CREATE TYPE grant_status AS ENUM (
    'potential',
    'reviewing',
    'drafting',
    'submitted',
    'approved',
    'rejected'
);

-- Create tables
CREATE TABLE IF NOT EXISTS organisation_profiles (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name VARCHAR(255) NOT NULL,
    description TEXT,
    mission TEXT,
    vision TEXT,
    registration_number VARCHAR(100),
    registration_date DATE,
    annual_income DECIMAL(15,2),
    staff_count INTEGER,
    volunteer_count INTEGER,
    focus_areas JSONB DEFAULT '[]',
    target_beneficiaries JSONB DEFAULT '[]',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    user_id UUID REFERENCES auth.users NOT NULL
);

CREATE TABLE IF NOT EXISTS grants (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    title VARCHAR(255) NOT NULL,
    funder VARCHAR(255) NOT NULL,
    description TEXT,
    eligibility_criteria TEXT,
    amount_range JSONB,
    due_date TIMESTAMP WITH TIME ZONE,
    source_url TEXT,
    guidelines_url TEXT,
    status grant_status DEFAULT 'potential',
    eligibility_analysis JSONB,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS grant_applications (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    grant_id UUID REFERENCES grants NOT NULL,
    organisation_id UUID REFERENCES organisation_profiles NOT NULL,
    status grant_status DEFAULT 'drafting',
    submitted_at TIMESTAMP WITH TIME ZONE,
    eligibility_score DECIMAL(3,2),
    eligibility_notes TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS application_documents (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    application_id UUID REFERENCES grant_applications NOT NULL,
    name VARCHAR(255) NOT NULL,
    type VARCHAR(50),
    storage_path TEXT NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Create indexes
CREATE INDEX idx_grants_funder ON grants(funder);
CREATE INDEX idx_grants_due_date ON grants(due_date);
CREATE INDEX idx_grant_applications_grant_id ON grant_applications(grant_id);
CREATE INDEX idx_grant_applications_organisation_id ON grant_applications(organisation_id);

-- Create RLS policies
ALTER TABLE organisation_profiles ENABLE ROW LEVEL SECURITY;
ALTER TABLE grants ENABLE ROW LEVEL SECURITY;
ALTER TABLE grant_applications ENABLE ROW LEVEL SECURITY;
ALTER TABLE application_documents ENABLE ROW LEVEL SECURITY;

-- Organisation profiles policies
CREATE POLICY "Users can view their own organisation profile"
    ON organisation_profiles FOR SELECT
    USING (auth.uid() = user_id);

CREATE POLICY "Users can update their own organisation profile"
    ON organisation_profiles FOR UPDATE
    USING (auth.uid() = user_id);

CREATE POLICY "Users can create their own organisation profile"
    ON organisation_profiles FOR INSERT
    WITH CHECK (auth.uid() = user_id);

-- Grants policies (publicly readable)
CREATE POLICY "Anyone can view grants"
    ON grants FOR SELECT
    USING (true);

-- Grant applications policies
CREATE POLICY "Users can view their own applications"
    ON grant_applications FOR SELECT
    USING (EXISTS (
        SELECT 1 FROM organisation_profiles
        WHERE organisation_profiles.id = grant_applications.organisation_id
        AND organisation_profiles.user_id = auth.uid()
    ));

CREATE POLICY "Users can create applications for their organisation"
    ON grant_applications FOR INSERT
    WITH CHECK (EXISTS (
        SELECT 1 FROM organisation_profiles
        WHERE organisation_profiles.id = grant_applications.organisation_id
        AND organisation_profiles.user_id = auth.uid()
    ));

-- Application documents policies
CREATE POLICY "Users can view their own documents"
    ON application_documents FOR SELECT
    USING (EXISTS (
        SELECT 1 FROM grant_applications
        JOIN organisation_profiles ON grant_applications.organisation_id = organisation_profiles.id
        WHERE application_documents.application_id = grant_applications.id
        AND organisation_profiles.user_id = auth.uid()
    ));

CREATE POLICY "Users can create documents for their applications"
    ON application_documents FOR INSERT
    WITH CHECK (EXISTS (
        SELECT 1 FROM grant_applications
        JOIN organisation_profiles ON grant_applications.organisation_id = organisation_profiles.id
        WHERE application_documents.application_id = grant_applications.id
        AND organisation_profiles.user_id = auth.uid()
    )); 