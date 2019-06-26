# frozen_string_literal: true

require 'json'
require 'awspec'

config = JSON.parse(File.read('../profile.json'))

describe s3_bucket(config['prefix'] + '-key-value-store') do
  it { should exist }
  it { should have_versioning_enabled }
  it { should have_tag('pipeline').value('bootstrap-aws/key-value-store') }
end

describe iam_role('AccessBootstrapKeyValueStoreRole') do
  it { should exist }
  it { should be_allowed_action('s3:ListBucket').resource_arn('arn:aws:s3:::' + config['prefix'] + '-key-value-store') }
  it { should be_allowed_action('s3:PutObject').resource_arn('arn:aws:s3:::' + config['prefix'] + '-key-value-store/*') }
  it { should be_allowed_action('s3:GetObject').resource_arn('arn:aws:s3:::' + config['prefix'] + '-key-value-store/*') }
  it { should be_allowed_action('s3:DeleteObject').resource_arn('arn:aws:s3:::' + config['prefix'] + '-key-value-store/*') }
  it { should_not be_allowed_action('s3:GetObjectAcl').resource_arn('arn:aws:s3:::' + config['prefix'] + '-key-value-store/*') }
end
