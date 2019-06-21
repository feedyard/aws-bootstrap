# frozen_string_literal: true

require 'json'
require 'awspec'

config = JSON.parse(File.read('../bootstrap.json'))

describe s3_bucket(config['prefix'] + '-key-value-store') do
  it { should exist }
  it { should have_versioning_enabled }
  it { should have_tag('pipeline').value('bootstrap-aws/key-value-store') }
end
