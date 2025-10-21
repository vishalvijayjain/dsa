# COS Bring-Up Guide

## 1. Overview

This document describes the process to **bring up a COS Host** using information from **NetBox** and **NCS-API-based configuration rendering**.
The goal is to generate the **day0 YAML input** for an NCS COS host, with minimal manual input in the API request and NetBox Config Context.

---

## 2. Assumptions (Common to All Service Groups)

* Each interface configuration is defined in the **NetBox Config Context**.
* Interface topology comes from **NetBox Device Interfaces** — each interface defined in the Config Context must be connected.
* **Bundle (LAG)** information will be read from NetBox Device Interface data.
* **Bundle (MLAG)** information will be auto-generated.

  * MLAG will be configured only when a LAG contains interfaces connected to both devices of an MLAG pair.
* If a **BGP peering SVI** is provided and not found, it will be created from scratch.

  * The subnet and VLAN will be reserved and created in NetBox.
* If a **Layer 3 SVI** is provided and not found, it will be created only if the subnet is already reserved (by David Brown) and there is a NetBox prefix with the SVI name as the description. Otherwise, the bring-up will fail.
* If a **Layer 2 VLAN** is provided and not found, it will be created.

---

## 3. Bring-Up Workflow (COS Specific)

### Step 1. Prepare Host Configuration

1. Create or update the **NetBox Config Context** for the COS host.
   Config Contexts can be managed at:
   `https://us-east.dcim.test.cloud.ibm.com/extras/config-contexts/`

2. Define the interface and VLAN/SVI configuration under the `network_configuration` key.

   **Basic structure:**
   ```yaml
   network_configuration:
     interfaces:
       - name: <interface_name>
         access_configuration:
           name: <VLAN_or_SVI_name>
   ```

3. Add optional sections as needed:

   * `svi_bgp_info`: defines SVI BGP peering and tag (peer group).
   * `helper_addresses_info`: defines helper (DHCP) addresses on SVIs.
   * `svi_extentions`: list of SVI/VLAN names from other groups to be extended.

   **Complete structure:**
   ```yaml
   network_configuration:
     interfaces:
       - name: # Required
         speed: # Optional, when specific interface speed is needed
         # Port configuration for access port:
         access_configuration: # Required, in order to make the configuration explicit 
           name: # Required. It can be either a L2 VLAN name or an SVI name
         # Port configuration for trunk link:
         trunk_configuration: 
           vlans: # Required, in order to make the configuration explicit 
             - name: # Required. Name of the SVI to be allowed in the trunk, also can be L2 VLAN name
               native: # Optional, defaults to False. Flag to make this vlan native on the trunk (no tagging)
                      # Only one SVI can be marked native on a trunk, if more than one is found an error will be raised
     svi_bgp_info: # List of dictionaries, for SVI BGP peering creation
       - svi_name: # string, name of the SVI
         tag: # string, tag of the peering, determines the BGP group applied on the switch and the Host ASN
              # Can be one of: [uc_fabric_lb, uc_fabric_ntp, een_peering, netappv4, netappv6, cos_lb, 
              #                 netapp_file, netapp_block, netapp_intstor]
     svi_extentions: # List of strings, containing the SVI/VLAN names of other groups to be extended
     helper_addresses_info: # List of dictionaries, for defining helper addresses
       - svi_name: # string, name of the SVI to add helper address
         helper_addresses: # List of strings, each entry contains the IP address
   ```

**Important Notes:**

* The `svi_bgp_info` explicitly defines that an SVI will be used for BGP peering, and the tag determines the ASN and BGP group applied on the switch.
* The `helper_addresses` list provided will replace any existing helper address list on the same SVI. If the list is empty, no changes will happen and it will be ignored.
* The configuration schema follows RFC30 FAST-DS integration patterns with additional COS-specific extensions.

---

### Step 2. Verify NetBox Data

Before bring-up, ensure that NetBox has all required information for the host:

* **Interfaces connected** to **ToR** and **mToR** switches with correct names.
* **Correct bonding (LAG)** relationships for interfaces (bond information will be read from NetBox Device Interface data).
* **Hostname** and **device role** correctly defined.
* **Prefix info for L3 SVIs**: The subnet must exist in NetBox as a prefix with the SVI name as the description in the correct VRF. Prefix allocations for L3 SVIs must be requested by the Service Team to David Brown.

Example Host entry in NetBox:
`https://us-east.dcim.test.cloud.ibm.com/dcim/devices/42528/`

Example Config Context:
`https://us-east.dcim.test.cloud.ibm.com/extras/config-contexts/103/`

**Expected NetBox Device Interface Data:**

All interfaces defined in the Config Context must be connected to the correct switches/ports with correct names. For example:

```json
{
  "hostname": "dal2-qz4-sr7-rk028-s02",
  "interfaces": [
    {
      "name": "enp3s0f1np0",
      "neighbor": "tor28.1a.cos.qz4.sr07.dal09",
      "neighbor_interface": "Ethernet29/1",
      "bond": 1
    },
    {
      "name": "enp3s0f1np1",
      "neighbor": "tor28.1b.cos.qz4.sr07.dal09",
      "neighbor_interface": "Ethernet29/1",
      "bond": 1
    },
    {
      "name": "enp4s0f1np0",
      "neighbor": "tor28.1a.cos.qz4.sr07.dal09",
      "neighbor_interface": "Ethernet30/1",
      "bond": 2
    },
    {
      "name": "enp4s0f1np1",
      "neighbor": "tor28.1b.cos.qz4.sr07.dal09",
      "neighbor_interface": "Ethernet30/1",
      "bond": 2
    },
    {
      "name": "eth0",
      "neighbor": "mtor28.1a.cos.qz4.sr07.dal09",
      "neighbor_interface": "Ethernet45",
      "bond": 0
    },
    {
      "name": "eth1",
      "neighbor": "mtor28.1b.cos.qz4.sr07.dal09",
      "neighbor_interface": "Ethernet45",
      "bond": 0
    },
    {
      "name": "mgmt0",
      "neighbor": "mtor28.1a.cos.qz4.sr07.dal09",
      "neighbor_interface": "Ethernet46"
    }
  ]
}
```

**Critical Requirements:**
* All interfaces must be connected to the correct switches/ports
* Bond information is required when the server has multiple different bonds on the ToRs
* Unconnected or undefined interfaces will cause bring-up to fail

---

### Step 3. Generate COS Host Configuration

Send a request to the configuration generation API with the required host information.

**Request payload (minimum required):**

```yaml
nodes:
  - uuid: e5aba870-d5a2-4e1a-959e-2cd7e4ce945e
    provisioning_role: cos_accessor
```

The API will return a generated **day0 YAML configuration** for the COS host, containing interfaces, VLANs, MLAG, and BGP peering data.

---

### Step 4. Validate and Deploy

1. **Validate the generated configuration:**

   * Ensure all interfaces are connected as per NetBox.
   * Verify VLAN/SVI mapping correctness.
   * Check that MLAG and LAG bundles are properly configured.
   * Confirm prefix information matches NetBox prefixes (IMPORTANT: description must match SVI name).
   
2. **Deploy the configuration** via the provisioning system (NCS pipeline).

3. **Post-deployment verification:**

   * Interfaces and MLAGs are up.
   * VLANs and SVIs exist and match NetBox.
   * BGP sessions form successfully (if configured).
   * Helper addresses are configured correctly (if specified).

---

## 4. Complete COS Configuration Example

### Config Context Example (with prefix information)

```json
{
  "network_configuration": {
    "interfaces": [
      {
        "name": "mgmt0",
        "access_configuration": {
          "name": "US_BOUNDARY_UNDERCLOUD_IPMI_VLAN"
        },
        "prefix": {
          "tag": null,
          "vlan": "US_BOUNDARY_UNDERCLOUD_IPMI_VLAN",
          "vrf": "DEFAULT"
        }
      },
      {
        "name": "eth0",
        "access_configuration": {
          "name": "US_BOUNDARY_INTERNAL_COS_SVI"
        },
        "prefix": {
          "tag": null,
          "vlan": "US_BOUNDARY_INTERNAL_COS_SVI",
          "vrf": "US_BOUNDARY_INTERNAL"
        }
      },
      {
        "name": "eth1",
        "access_configuration": {
          "name": "US_BOUNDARY_INTERNAL_COS_SVI"
        },
        "prefix": {
          "tag": null,
          "vlan": "US_BOUNDARY_INTERNAL_COS_SVI",
          "vrf": "US_BOUNDARY_INTERNAL"
        }
      },
      {
        "name": "enp3s0f1np0",
        "access_configuration": {
          "name": "US_BOUNDARY_COS_GROUP_LOCAL_SVI"
        },
        "prefix": {
          "tag": null,
          "vlan": "US_BOUNDARY_COS_GROUP_LOCAL_SVI",
          "vrf": "US_BOUNDARY_COS_GROUP_LOCAL"
        }
      },
      {
        "name": "enp3s0f1np1",
        "access_configuration": {
          "name": "US_BOUNDARY_COS_GROUP_LOCAL_SVI"
        },
        "prefix": {
          "tag": null,
          "vlan": "US_BOUNDARY_COS_GROUP_LOCAL_SVI",
          "vrf": "US_BOUNDARY_COS_GROUP_LOCAL"
        }
      },
      {
        "name": "enp4s0f1np0",
        "access_configuration": {
          "name": "US_BOUNDARY_COS_DATAPLANE_COS_SVI"
        },
        "prefix": {
          "tag": null,
          "vlan": "US_BOUNDARY_COS_DATAPLANE_COS_SVI",
          "vrf": "US_BOUNDARY_COS_DATAPLANE"
        }
      },
      {
        "name": "enp4s0f1np1",
        "access_configuration": {
          "name": "US_BOUNDARY_COS_DATAPLANE_COS_SVI"
        },
        "prefix": {
          "tag": null,
          "vlan": "US_BOUNDARY_COS_DATAPLANE_COS_SVI",
          "vrf": "US_BOUNDARY_COS_DATAPLANE"
        }
      }
    ]
  }
}
```

### Resulting Host NCS Configuration (day0 YAML)

```yaml
- name: dal2-qz4-sr7-rk028-s02
  group_name: COS
  rack: dal09.sr07.rk28
  role: cos_accessor
  interfaces:
    - name: ipmi
      neighbor: mtor28.1a.cos.qz4.sr07.dal09
      neighbor_interface: Ethernet46
      neighbor_interface_config:
        access_configuration:
          vlan_name: US_BOUNDARY_UNDERCLOUD_IPMI_VLAN
    - name: eth0
      neighbor: mtor28.1a.cos.qz4.sr07.dal09
      neighbor_interface: Ethernet45
      mlag: True
      neighbor_interface_config:
        trunk_configuration:
          vlan_name_list:
            - name: US_BOUNDARY_INTERNAL_COS_SVI
              native: True
    - name: eth1
      neighbor: mtor28.1b.cos.qz4.sr07.dal09
      neighbor_interface: Ethernet45
      mlag: True
      neighbor_interface_config:
        trunk_configuration:
          vlan_name_list:
            - name: US_BOUNDARY_INTERNAL_COS_SVI
              native: True
    - name: enp3s0f1np0
      neighbor: tor28.1a.cos.qz4.sr07.dal09
      neighbor_interface: Ethernet29/1
      mlag: True
      port_channel: 1
      neighbor_interface_config:
        access_configuration:
          vlan_name: US_BOUNDARY_COS_GROUP_LOCAL_SVI
    - name: enp3s0f1np1
      neighbor: tor28.1b.cos.qz4.sr07.dal09
      neighbor_interface: Ethernet29/1
      mlag: True
      port_channel: 1
      neighbor_interface_config:
        access_configuration:
          vlan_name: US_BOUNDARY_COS_GROUP_LOCAL_SVI
    - name: enp4s0f1np0
      neighbor: tor28.1a.cos.qz4.sr07.dal09
      neighbor_interface: Ethernet30/1
      mlag: True
      port_channel: 2
      neighbor_interface_config:
        access_configuration:
          vlan_name: US_BOUNDARY_COS_DATAPLANE_COS_SVI
    - name: enp4s0f1np1
      neighbor: tor28.1b.cos.qz4.sr07.dal09
      neighbor_interface: Ethernet30/1
      mlag: True
      port_channel: 2
      neighbor_interface_config:
        access_configuration:
          vlan_name: US_BOUNDARY_COS_DATAPLANE_COS_SVI
```

---

## 5. Modifying Existing Host Configuration

Since NetBox Config Contexts define the host's network configuration, modifying a host can be achieved by:

1. Modifying the existing Config Context, OR
2. Creating a new Config Context and applying it to the host

After modifying the Config Context, rerun the API request with the same payload to regenerate the configuration.

---

## 6. Configuration Approach Benefits

### Config Context vs Jinja Templates

**Using Jinja Templates:**
* Makes each host configuration static
* Provides no control over interface configuration (hardcoded in template)
* Only the topology changes (pulled from NetBox)

**Using NetBox Config Context (Current Approach):**
* All interface configurations can be defined dynamically inside the Config Context
* Topology is defined dynamically in NetBox
* Provides flexibility and control without code changes
* Easier to maintain and modify per-host configurations

---

## 7. Troubleshooting and Escalation

If the NCS job fails during the bring-up process, follow these steps to gather diagnostic information for escalation.

### Step 1: Check Workflow State

Use the FAST-DS API to monitor the workflow state. The workflow will show various stages including `WAITING FOR IP ASSIGNMENT`, `NCS WAIT - ADD HOST`, and eventually `WORKFLOW COMPLETED` or error states.

```bash
export ID=<workflow_id>
while true; do 
  curl -k -X 'GET' "https://<fast-ds-host>/api/Workflow/report/$ID" \
    -H 'accept: */*' \
    -H 'Content-Type: application/json' | jq
  sleep 5
done
```

**Look for the following in the output:**
* `WorkflowState`: Current state of the workflow
* `WorkflowErrorDetail`: Any error messages
* `NcsJobId`: The NCS Job ID (needed for further troubleshooting)
* `FailedNodes`: Any nodes that failed during provisioning

Example output:
```json
{
  "WorkflowId": "c1fdcc20-593e-4e97-9629-3423b60b50af",
  "Active": true,
  "WorkflowState": "NCS WAIT - ADD HOST",
  "WorkflowErrorDetail": "",
  "NcsJobId": "2025:01:30:12:09:07_3d9e4532-5dc6-4919-b9a5-c5951855c84f",
  "FailedNodes": []
}
```

### Step 2: Retrieve NCS Job ID

Once the workflow reaches NCS, an NCS Job ID will be generated. Extract this from the workflow status:

```json
"NcsJobId": "2025:01:30:12:09:07_3d9e4532-5dc6-4919-b9a5-c5951855c84f"
```

### Step 3: Gather Job Information from Odyssey Container

From the Odyssey container, use the following utilities to collect detailed job information:

#### Get Job Status

```bash
get_job --jid "2025:01:30:12:09:07_3d9e4532-5dc6-4919-b9a5-c5951855c84f"
```

Output shows:
* `completion_status`: SUCCESS/FAILED
* `run_status`: COMPLETED/FAILED
* `job_name`: Type of job (e.g., "API adding Host")
* `start_time` and `end_time`

#### Get Job Output

```bash
get_job_output --jid "2025:01:30:12:09:07_3d9e4532-5dc6-4919-b9a5-c5951855c84f"
```

This shows:
* Configuration changes applied to each switch (ToR and mToR)
* Diff output showing what was added/modified
* Success/failure status per device
* Any error messages

#### Get Job Logs

```bash
get_job_logs --jid "2025:01:30:12:09:07_3d9e4532-5dc6-4919-b9a5-c5951855c84f"
```

This provides detailed step-by-step logs including:
* Host configuration rendering
* Validation steps
* Configuration push to devices
* Any errors encountered

### Step 4: Create NFP Ticket for Escalation

When creating an NFP ticket for escalation, include the following information:

**Required Information:**
1. **Workflow ID**: The FAST-DS workflow ID
2. **NCS Job ID**: From the workflow status output
3. **Node UUID**: The device UUID from NetBox
4. **Provisioning Role**: The role specified in the API request (e.g., `cos_accessor`)
5. **Job Status Output**: Paste the output from `get_job`
6. **Job Logs**: Paste relevant sections from `get_job_logs`
7. **Job Output**: Paste the output from `get_job_output` (if available)
8. **Error Details**: Any `WorkflowErrorDetail` or error messages from logs
9. **NetBox Links**: 
   * Device URL
   * Config Context URL
10. **Configuration Details**:
    * Failed interface(s)
    * VLAN/SVI name(s) involved
    * Any missing or incorrect NetBox data identified

**Example Ticket Format:**

```
Subject: COS Host Bring-Up Failed - <hostname>

Environment: <qz4-dal09 / production environment>
Workflow ID: c1fdcc20-593e-4e97-9629-3423b60b50af
NCS Job ID: 2025:01:30:12:09:07_3d9e4532-5dc6-4919-b9a5-c5951855c84f
Device UUID: 5e47383c-14e1-4d0b-93fe-29ae29c7012f
Provisioning Role: cos_accessor
NetBox Device: https://us-east.dcim.test.cloud.ibm.com/dcim/devices/42528/
Config Context: https://us-east.dcim.test.cloud.ibm.com/extras/config-contexts/103/

Issue Description:
[Describe what failed - e.g., "Interface enp3s0f1np0 configuration failed on tor28.1a"]

Job Status:
[Paste get_job output]

Error Details:
[Paste relevant error messages from get_job_logs]

Job Output:
[Paste get_job_output showing the failure]

Additional Context:
[Any other relevant information]
```

---

## 8. Notes and Important Reminders

* **COS hosts use both ToR and mToR connections**, typically requiring MLAG for redundancy.
* **Accurate NetBox cabling and prefix data are critical** — mismatches will cause generation errors.
* **Unconnected or undefined interfaces will cause bring-up to fail.**
* **Prefix allocations for L3 SVIs** must be requested to David Brown before bring-up.
* **NetBox prefix description must exactly match the SVI name** for L3 SVIs.
* When defining **helper addresses**, the provided list will replace all existing helper addresses on that SVI.
* For **BGP peering SVIs**, ensure the correct tag is specified in `svi_bgp_info` to apply the proper BGP group and ASN.
* The configuration schema follows **RFC30 FAST-DS integration patterns** available at: `https://github.ibm.com/bedrock-squad/ng-fabric-internal-guidance/blob/main/rfc/rfc30_fast-ds_integration_patterns.md`

---

## 9. Reference Links

* **NetBox Config Contexts:** `https://us-east.dcim.test.cloud.ibm.com/extras/config-contexts/`
* **Example COS Host (dal2-qz4-sr7-rk028-s02):** `https://us-east.dcim.test.cloud.ibm.com/dcim/devices/42528/`
* **Example Config Context:** `https://us-east.dcim.test.cloud.ibm.com/extras/config-contexts/103/`
* **Odyssey Day2 Repository:** `https://github.ibm.com/neteng/odyssey-day2-additions`