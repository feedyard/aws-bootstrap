# frozen_string_literal: true

require 'spec_helper'

config = JSON.parse(File.read('../bootstrap.json'))

describe s3_bucket(config['prefix'] + '-' + ENV['PROFILE'] + '-tf-state') do
  it { should exist }
  it { should have_versioning_enabled }
  it { should have_tag('pipeline').value('aws-bootstrap/secure-state-store') }
end
