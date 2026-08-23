import { defineMsdmdCollection } from "./skill-lib/msdmd/collection";

export default defineMsdmdCollection({
  "repo": "The-Interdependency/stack",
  "source_commit": "stack-manifest:720b2d842252d20a31a04bfb13e7e918bfdabe646497e61615cf529ad70b12a3",
  "declarations": [
    {
      "file": "skill-lib/skill-lib_msdmd.ts",
      "block": "MODULE_BUILD",
      "id": "stack_skill_lib_msdmd_collection",
      "fields": {
        "module_name": "skill-lib MSDMD collection",
        "module_kind": "archive-index",
        "repository": "The-Interdependency/skill-lib",
        "stack_path": "skill-lib",
        "collection_point": "skill-lib/skill-lib_msdmd.ts",
        "archive_status": "archived-source-tree",
        "source_commit": "fb3b53a7629f7f03ecf255167d52c13abef1a979",
        "source_tree_git_sha1": "859a9f4cddea0937579f0fb48a36bce4c1a19c99",
        "tree_sha256": "a1a89697b9722b1e3897e83b0ff465adb7e0832a9068080c0ef429b0edcf27a9",
        "summary": "root stack pointer to the archived skill-lib repo-level MSDMD collection point"
      }
    },
    {
      "file": "research/metapat/metapat_msdmd.ts",
      "block": "MODULE_BUILD",
      "id": "stack_metapat_msdmd_collection",
      "fields": {
        "module_name": "metapat MSDMD collection",
        "module_kind": "archive-index",
        "repository": "The-Interdependency/metapat",
        "stack_path": "research/metapat",
        "collection_point": "research/metapat/metapat_msdmd.ts",
        "archive_status": "archived-source-tree",
        "source_commit": "34d954aa1e2092e615b03a180500f6b6977f501e",
        "source_tree_git_sha1": "9d83b8bb393a7420062c5049cfa2baa572336ace",
        "tree_sha256": "bc91150d10edba747a779e29da4428c1a5eab7dc7a5ee8a0ae40c6a5118581ae",
        "summary": "root stack pointer to the archived metapat repo-level MSDMD collection point"
      }
    },
    {
      "file": "research/ucns/ucns_msdmd.ts",
      "block": "MODULE_BUILD",
      "id": "stack_ucns_msdmd_collection",
      "fields": {
        "module_name": "ucns MSDMD collection",
        "module_kind": "archive-index",
        "repository": "The-Interdependency/ucns",
        "stack_path": "research/ucns",
        "collection_point": "research/ucns/ucns_msdmd.ts",
        "archive_status": "archived-source-tree",
        "source_commit": "1975fe70cf4e0826a8020c2da3047569e277af64",
        "source_tree_git_sha1": "06c2fe6cf2e148d610808c6f00f4a26e85f43d62",
        "tree_sha256": "a6fa5a674950b1847738c48e57c7df2e8727c8951db16b698318fe2ca9611d65",
        "stack_overlay_paths": "research/ucns/ucns_msdmd.ts",
        "summary": "root stack pointer to the stack-local UCNS repo-level MSDMD collection overlay"
      }
    },
    {
      "file": "research/edcm/edcm_msdmd.ts",
      "block": "MODULE_BUILD",
      "id": "stack_edcm_msdmd_collection",
      "fields": {
        "module_name": "edcm MSDMD collection",
        "module_kind": "archive-index",
        "repository": "The-Interdependency/edcm",
        "stack_path": "research/edcm",
        "collection_point": "research/edcm/edcm_msdmd.ts",
        "archive_status": "archived-source-tree",
        "source_commit": "7951ca32ba0f2494dc68ff9b7f6a80151918a56d",
        "source_tree_git_sha1": "92e7fd2040a6d8b162636083739e1927cac8326b",
        "tree_sha256": "61426c7d592b2376cce03bff12e8fbb07a857ccddcd1fe411ff4b00d2cec3afa",
        "summary": "root stack pointer to the archived edcm repo-level MSDMD collection point"
      }
    },
    {
      "file": "research/pcea/pcea_msdmd.ts",
      "block": "MODULE_BUILD",
      "id": "stack_pcea_msdmd_collection",
      "fields": {
        "module_name": "pcea MSDMD collection",
        "module_kind": "archive-index",
        "repository": "The-Interdependency/pcea",
        "stack_path": "research/pcea",
        "collection_point": "research/pcea/pcea_msdmd.ts",
        "archive_status": "archived-source-tree",
        "source_commit": "4d2c581448b97bfb71da92b35487e74e6e3bcedc",
        "source_tree_git_sha1": "521b26b36692ca91baa73ef65d5314efbc7c9cba",
        "tree_sha256": "173b5f8c27eeb54744f0cf9ddd406afa5f7a7a533ad8e4bf649c490dcb908f63",
        "summary": "root stack pointer to the archived pcea repo-level MSDMD collection point"
      }
    },
    {
      "file": "research/ptcna/ptcna_msdmd.ts",
      "block": "MODULE_BUILD",
      "id": "stack_ptcna_msdmd_collection",
      "fields": {
        "module_name": "ptcna MSDMD collection",
        "module_kind": "archive-index",
        "repository": "The-Interdependency/ptcna",
        "stack_path": "research/ptcna",
        "collection_point": "research/ptcna/ptcna_msdmd.ts",
        "archive_status": "archived-source-tree",
        "source_commit": "97abdd1bbda61a68e0aac8595a32a3cb0ce73487",
        "source_tree_git_sha1": "0820e25698b8fdefa41da635a5d5dc43b230b396",
        "tree_sha256": "1610b6d24391989472476ae2f38dd5574f31a4af3efb454d9ce458fd28d750a1",
        "summary": "root stack pointer to the archived ptcna repo-level MSDMD collection point"
      }
    }
  ],
  "gaps": [],
  "edges": [
    {
      "from": "stack_skill_lib_msdmd_collection",
      "to": "The-Interdependency/skill-lib",
      "kind": "indexes",
      "source_block": "MODULE_BUILD",
      "source_id": "stack_skill_lib_msdmd_collection"
    },
    {
      "from": "stack_metapat_msdmd_collection",
      "to": "The-Interdependency/metapat",
      "kind": "indexes",
      "source_block": "MODULE_BUILD",
      "source_id": "stack_metapat_msdmd_collection"
    },
    {
      "from": "stack_ucns_msdmd_collection",
      "to": "The-Interdependency/ucns",
      "kind": "indexes",
      "source_block": "MODULE_BUILD",
      "source_id": "stack_ucns_msdmd_collection"
    },
    {
      "from": "stack_edcm_msdmd_collection",
      "to": "The-Interdependency/edcm",
      "kind": "indexes",
      "source_block": "MODULE_BUILD",
      "source_id": "stack_edcm_msdmd_collection"
    },
    {
      "from": "stack_pcea_msdmd_collection",
      "to": "The-Interdependency/pcea",
      "kind": "indexes",
      "source_block": "MODULE_BUILD",
      "source_id": "stack_pcea_msdmd_collection"
    },
    {
      "from": "stack_ptcna_msdmd_collection",
      "to": "The-Interdependency/ptcna",
      "kind": "indexes",
      "source_block": "MODULE_BUILD",
      "source_id": "stack_ptcna_msdmd_collection"
    }
  ]
});
