import boto3
import json
import os

def list_ai_policies():
    # Create a Boto3 client for AWS Organizations
    client = boto3.client('organizations')

    # Retrieve the list of AI service opt-out policies
    response = client.list_policies(Filter='AISERVICES_OPT_OUT_POLICY')

    # Extract the list of policies
    ai_policies = response['Policies']

    # Find the output folder path
    current_directory = os.getcwd()
    output_folder = os.path.join(current_directory, 'output', 'Policies', 'aiPolicies')

    # Create the output folder if it doesn't exist
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Get the details of each AI policy
    for ai_policy in ai_policies:
        policy_id = ai_policy['Id']
        policy_name = ai_policy['Name']

        # Retrieve the policy content
        policy_response = client.describe_policy(PolicyId=policy_id)
        policy_content_str = policy_response['Policy']['Content']

        # Create a separate JSON file for each AI policy in the output folder
        policy_file_name = os.path.join(output_folder, f"{policy_name}.json")

        # Load the policy content as JSON to format it
        policy_content = json.loads(policy_content_str)

        # Write the formatted policy content to the JSON file
        with open(policy_file_name, 'w') as file:
            json.dump(policy_content, file, indent=4)

        print(f"JSON file generated for policy '{policy_name}'.")

