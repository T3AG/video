# Copyright 2014 Google Inc. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""Command for deleting snapshots."""
from __future__ import absolute_import
from __future__ import unicode_literals
from googlecloudsdk.api_lib.compute import base_classes
from googlecloudsdk.api_lib.compute import utils
from googlecloudsdk.calliope import base
from googlecloudsdk.command_lib.compute import flags as compute_flags
from googlecloudsdk.command_lib.compute.snapshots import flags


class Delete(base.DeleteCommand):
  """Delete Google Compute Engine snapshots.

  *{command}* deletes one or more Google Compute Engine snapshots.
  """

  @staticmethod
  def Args(parser):
    Delete.SnapshotArg = flags.MakeSnapshotArg(plural=True)
    Delete.SnapshotArg.AddArgument(parser, operation_type='delete')

  def Run(self, args):
    holder = base_classes.ComputeApiHolder(self.ReleaseTrack())
    client = holder.client

    snapshot_refs = Delete.SnapshotArg.ResolveAsResource(
        args,
        holder.resources,
        scope_lister=compute_flags.GetDefaultScopeLister(client))

    utils.PromptForDeletion(snapshot_refs)

    requests = []
    for snapshot_ref in snapshot_refs:
      requests.append((client.apitools_client.snapshots, 'Delete',
                       client.messages.ComputeSnapshotsDeleteRequest(
                           project=snapshot_ref.project,
                           snapshot=snapshot_ref.snapshot)))

    return client.MakeRequests(requests)
