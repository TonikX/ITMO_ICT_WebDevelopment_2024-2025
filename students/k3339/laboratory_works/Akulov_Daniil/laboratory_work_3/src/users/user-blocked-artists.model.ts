import {Column, DataType, ForeignKey, Model, Table} from "sequelize-typescript";
import {ApiProperty} from "@nestjs/swagger";
import {User} from "./users.model";
import {Artist} from "../artists/artists.model";

@Table({tableName: 'user_blocked_artists', updatedAt: false})
export class UserBlockedArtists extends Model<UserBlockedArtists> {
    @ApiProperty({example: 1})
    @Column({type: DataType.INTEGER, unique: true, autoIncrement: true, primaryKey: true})
    id: number

    @ForeignKey(() => User)
    @Column({type: DataType.INTEGER})
    userId: number

    @ForeignKey(() => Artist)
    @Column({type: DataType.INTEGER})
    artistId: number
}