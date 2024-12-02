import {BelongsToMany, Column, DataType, Model, Table} from "sequelize-typescript";
import {ApiProperty} from "@nestjs/swagger";
import {User} from "../users/users.model";
import {UserBlockedArtists} from "../users/user-blocked-artists.model";
import {Album} from "../albums/albums.model";
import {AlbumArtists} from "../albums/album-artists.model";

interface ArtistCreationAttrs{
    username:string;
    name:string;
    password:string;
}

@Table({tableName: 'artists'})
export class Artist extends Model<Artist, ArtistCreationAttrs> {
    @ApiProperty({example: 1})
    @Column({type: DataType.INTEGER, unique: true, autoIncrement: true, primaryKey: true})
    id: number

    @ApiProperty({example: 'rileyparker'})
    @Column({type: DataType.STRING(20), unique: true, allowNull: false})
    username: string

    @ApiProperty({example: 'Riley Parker'})
    @Column({type: DataType.STRING(50), allowNull: false})
    name: string

    @ApiProperty({example: 'password123'})
    @Column({type: DataType.STRING, allowNull: false})
    password: string

    @ApiProperty({example: 'Artist profile desc :)'})
    @Column({type: DataType.STRING(140), defaultValue: ''})
    description: string

    @ApiProperty({example: 'ovbisut94ueslxzjvo.png'})
    @Column({type: DataType.STRING, defaultValue: ''})
    avatarURL: string

    @BelongsToMany(() => User, () => UserBlockedArtists)
    usersBlocks: User[]

    @BelongsToMany(() => Album, () => AlbumArtists)
    albums: User[]
}